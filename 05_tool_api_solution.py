import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.5-flash")

if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env file.")

client = genai.Client(api_key=API_KEY)
app = FastAPI(title="Week 1 Day 5 — Tool-Calling Support API")

MOCK_ORDERS = {
    "ORD-101": {"status": "Delivered", "item": "Mechanical Keyboard", "delivered_on": "2026-11-24"},
    "ORD-102": {"status": "Shipped", "item": "27-inch 4K Monitor", "eta": "2026-11-29", "carrier": "BlueDart"},
    "ORD-103": {"status": "Processing", "item": "USB-C Docking Station", "eta": "2026-12-01"},
    "ORD-104": {"status": "Cancelled", "item": "Wireless Mouse", "refund_status": "Refunded to card"},
}


def get_order_status(order_id: str) -> dict:
    """Look up the live shipping and fulfillment status of a customer order by its order ID (e.g., ORD-101)."""
    clean_id = order_id.strip().upper()
    if clean_id in MOCK_ORDERS:
        return {"found": True, "order_id": clean_id, **MOCK_ORDERS[clean_id]}
    return {"found": False, "order_id": clean_id, "message": "Order ID not found in database."}


TOOL_REGISTRY = {
    "get_order_status": get_order_status,
}

SYSTEM_PROMPT = """
You are a helpful e-commerce customer support assistant.
- Use the `get_order_status` tool whenever a user asks about a specific order ID.
- Never guess or invent order statuses. If the tool returns found=False, politely tell the customer the order ID was not found.
- For general questions that do not require an order lookup, answer concisely without calling any tool.
"""


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Customer question")


class AskResponse(BaseModel):
    answer: str
    tool_called: str | None = None
    tool_args: dict | None = None
    tool_result: dict | None = None
    latency_ms: float


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    reraise=True,
)
def generate_with_tools(contents: list, config: types.GenerateContentConfig):
    return client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/ask", response_model=AskResponse)
def ask_assistant(payload: AskRequest):
    start = time.perf_counter()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.0,
        tools=[get_order_status],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=payload.question)])]

    try:
        first_response = generate_with_tools(contents, config)

        if first_response.function_calls:
            fc = first_response.function_calls[0]
            tool_name = fc.name
            tool_args = dict(fc.args) if fc.args else {}

            if tool_name not in TOOL_REGISTRY:
                raise HTTPException(status_code=400, detail=f"Unsupported tool: {tool_name}")

            tool_output = TOOL_REGISTRY[tool_name](**tool_args)

            contents.append(first_response.candidates[0].content)
            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=tool_name,
                            response={"result": tool_output},
                        )
                    ],
                )
            )
            second_response = generate_with_tools(contents, config)
            final_answer = (second_response.text or "").strip()
            latency_ms = (time.perf_counter() - start) * 1000
            return AskResponse(
                answer=final_answer,
                tool_called=tool_name,
                tool_args=tool_args,
                tool_result=tool_output,
                latency_ms=round(latency_ms, 1),
            )

        final_answer = (first_response.text or "").strip()
        latency_ms = (time.perf_counter() - start) * 1000
        return AskResponse(
            answer=final_answer,
            tool_called=None,
            tool_args=None,
            tool_result=None,
            latency_ms=round(latency_ms, 1),
        )
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=502, detail=f"LLM service error: {err}")

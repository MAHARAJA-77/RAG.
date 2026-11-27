# Day 5 Engineering Tasks: Tool Calling, FastAPI & Squad Lock-In

## Important Ground Rules
- Use your personal free-tier API key (`GEMINI_API_KEY` in `.env`). Keep `.env`, `.venv/`, and `chroma_db/` ignored by Git.
- **15-Minute Rule:** Spend 15 minutes reading tracebacks and testing payloads in Swagger UI (`/docs`) yourself before asking for a hint.

---

## Morning & Early Afternoon Build (`05_tool_api.py` — Due 03:15 PM)
1. **Define the Order Lookup Tool (`TODO 1`):** Write a crisp docstring inside `get_order_status(order_id: str) -> dict` (Gemini reads the function name, type hints, and docstring to decide when to invoke the tool). Normalize `order_id.strip().upper()` so lowercase inputs like `"ord-101"` still match.
2. **Add Retry Resilience (`TODO 2`):** Decorate `generate_with_tools()` with `@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)`.
3. **Implement Two-Step Manual Tool Execution (`TODO 3`):**
   - Call `generate_with_tools()` with `tools=[get_order_status]`, `temperature=0.0`, and `automatic_function_calling` disabled.
   - If `first_response.function_calls` is present, execute the Python function via `TOOL_REGISTRY`, append `first_response.candidates[0].content` and `types.Part.from_function_response(...)` to `contents`, and run a second generation pass to compose the final natural-language answer.
   - If no tool call is requested, return `first_response.text` directly with `tool_called=None`.
4. **Verify 4 Test Cases in Swagger UI (`http://127.0.0.1:8000/docs`):**
   - Start the server with `uvicorn 05_tool_api:app --reload`.
   - **Case 1 (Valid Order):** `"Where is my order ORD-102?"` -> `tool_called="get_order_status"`, returns shipped tracking details.
   - **Case 2 (Unknown Order):** `"Check status for ORD-999"` -> `tool_called="get_order_status"`, politely reports order not found without hallucinating.
   - **Case 3 (General Question):** `"What are your support hours?"` -> `tool_called=null`, answers directly without invoking the tool.
   - **Case 4 (Validation Error):** Empty string `""` -> automatically rejected by `Pydantic` `Field(min_length=1)` with HTTP `422`.
5. **Final Week 1 Git Push:** Commit and push `05_tool_api.py` to your personal bootcamp repository before **03:15 PM**.

---

## Afternoon Squad Pairing & Weekend Prep (03:15 PM – 05:00 PM)
1. **Form 3 Engineering Squads:** Join your assigned squad (two squads of 3 interns + one squad of 4 interns) and review `PROJECT_SELECTION_AND_ROLES.md`.
2. **Select Project & Lock Roles:** Claim one unique project from the 5-project menu and assign **Member A (Data, Ingestion & Tools)**, **Member B (Prompts, Retrieval & Guardrails)**, and **Member C (Backend API, Eval & UI)**.
3. **Create Shared Squad Repository:** Initialize one new GitHub repo per squad with `.gitignore` configured *first*, add all teammates as collaborators, and create three feature branches: `feat/data-tools`, `feat/prompts-rag`, and `feat/api-ui`.
4. **Weekend Dataset Collection (Days 6–7 Async):** Gather and clean the raw sample files required for your squad's project so ingestion starts immediately on Monday at 09:30 AM.

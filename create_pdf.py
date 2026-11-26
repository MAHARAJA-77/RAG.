from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Create PDF file
pdf = canvas.Canvas("college_details.pdf", pagesize=A4)

# Add title
pdf.setFont("Helvetica-Bold", 20)
pdf.drawString(150, 800, "POPE'S COLLEGE")

# Add subtitle
pdf.setFont("Helvetica", 14)
pdf.drawString(150, 760, "Department of Information Technology")

# Add college information
pdf.setFont("Helvetica", 12)

pdf.drawString(50, 710, "Welcome to our College!")
pdf.drawString(50, 680, "Course: Information Technology")
pdf.drawString(50, 650, "Duration: 3 Years")
pdf.drawString(50, 620, "Subject: Generative AI")
pdf.drawString(50, 590, "Topic: Retrieval Augmented Generation")

# Save PDF
pdf.save()

print("PDF created successfully!")
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf():
    # Create a PDF document
    c = canvas.Canvas("sample.pdf", pagesize=letter)
    width, height = letter  # Get page dimensions
    
    # Add title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Tax Incentive Compliance Report")
    
    # Add version info
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Generated using ReportLab v{reportlab.__version__}")
    
    # Add some sample data
    c.drawString(100, height - 200, "• Client: ABC Corporation")
    c.drawString(100, height - 220, "• Period: Q4 2024")
    c.drawString(100, height - 240, "• Status: Compliant")
    
    # Save the PDF
    c.save()
    print(f"✅ Sample PDF created: sample.pdf")
    print(f"✅ ReportLab version: {reportlab.__version__}")

if __name__ == "__main__":
    create_sample_pdf()
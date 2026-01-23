from reportlab.pdfgen import canvas

def test_reportlab():
    try:
        # Create a simple PDF
        c = canvas.Canvas("test_output.pdf")
        c.drawString(100, 750, "ReportLab Test")
        c.drawString(100, 730, f"Version: {reportlab.__version__}")
        c.save()
        print("✅ ReportLab is working! PDF created: test_output.pdf")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    import reportlab
    print(f"ReportLab version: {reportlab.__version__}")
    test_reportlab()
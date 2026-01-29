from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(summary):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    text = p.beginText(40, 800)
    text.setFont("Helvetica", 12)

    text.textLine("Chemical Equipment Report")
    text.textLine("--------------------------")
    text.textLine("")
    text.textLine(f"Total Equipment: {summary['total_equipment']}")
    text.textLine(f"Average Flowrate: {summary['average_flowrate']}")
    text.textLine(f"Average Pressure: {summary['average_pressure']}")
    text.textLine(f"Average Temperature: {summary['average_temperature']}")

    if "type_distribution" in summary:
        text.textLine("")
        text.textLine("Equipment Type Distribution:")
        for k, v in summary["type_distribution"].items():
            text.textLine(f"- {k}: {v}")

    p.drawText(text)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

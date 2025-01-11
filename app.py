from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from io import BytesIO
from bidi.algorithm import get_display
from arabic_reshaper import reshape

class CustomPDF(FPDF):
    def __init__(self, date):
        super().__init__()
        self.date = date

    def header(self):
        top_margin = 10
        logo_width = 50  # Set the width of the logo
        x_position = self.w - logo_width - 10  # Subtract width and right margin (10 units)
        # Add logo
        try:
            self.image('logo.png', x=x_position, y=10, w=logo_width)  # Position the logo
        except FileNotFoundError:
            pass  # Skip if the logo is missing


        # Add title
        # self.set_font('Amiri', style='B', size=14)
        # self.cell(0, 10, txt="Tray", ln=True, align="C")

        # Add company details
        self.set_font('Amiri', size=10,)
        self.multi_cell(w=0, h=4.5, txt=process_arabic(
        "شركة الحلول الرقمية الرائدة لتقنية المعلومــــات\n"
        "المملكة العربية السعودية، الريـــــــــاض 12329\n"
        "شارع المهندس مساعد العنقري - حي السلمانية\n"
        "السجــــــــــل التجــــــــــــــاري: 1010853106"
        ), ln=True, align="J")

        # Add document date
        self.cell(0, 25, txt=process_arabic(f"تاريخ المستند: {self.date}"), ln=True, align="L")
        self.ln(-3)

    def footer(self):
        # Position footer at the bottom of the page
        self.set_y(-30)
        self.set_font('Amiri', size=8)

        # Footer content
        self.cell(0, 10, txt="Website: www.tray.com | Phone: +966-555-555-555 | Email: support@tray.com | Twitter: @TRAY_SAUDI | Instagram: @TRAY_SAUDI", ln=True, align="C")


def process_arabic(text):
    """Handle Arabic reshaping and BiDi rendering."""
    reshaped_text = reshape(text)
    return get_display(reshaped_text)

def generate_cover_letter(data):
    pdf = CustomPDF(date=data.get("date", "Unknown Date"))

    # Add fonts
    pdf.add_font("Amiri", fname="Amiri-Regular.ttf", uni=True)
    pdf.add_font("Amiri", style="B", fname="Amiri-Bold.ttf", uni=True)

    # Start creating the PDF
    pdf.add_page()

    # Set margins
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Add recipient and subject
    pdf.set_font("Amiri", style="B", size=12)
    pdf.cell(0, 10, txt=process_arabic(f"إلى: {data['recipient_name']}"), ln=True, align="R")
    pdf.cell(0, 10, txt=process_arabic(f"الموضوع: {data['subject']}"), ln=True, align="R")
    pdf.ln(10)

    # Add body text (from user input)
    pdf.set_font("Amiri", size=10)
    pdf.multi_cell(0, 10, txt=process_arabic(data["body"]), align="R")
    pdf.ln(10)

    # Add closing
    pdf.cell(0, 10, txt=process_arabic("فريق عمل Tray"), ln=True, align="R")

    # Generate and return PDF output
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Flask app setup
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "recipient_name": request.form["recipient_name"],
            "subject": request.form["subject"],
            "date": request.form["date"],
            "body": request.form["body"],
        }
        pdf_output = generate_cover_letter(data)
        return send_file(pdf_output, as_attachment=True, download_name="cover_letter.pdf", mimetype="application/pdf")

    return render_template("index.html")

def generate_report():
    # Logic for generating the report
    return "Report generated!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)

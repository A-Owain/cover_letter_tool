from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from io import BytesIO
from bidi.algorithm import get_display
from arabic_reshaper import reshape

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Test data for PDF
        recipient_name = request.form["recipient_name"]
        subject = request.form["subject"]
        
        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"To: {recipient_name}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Subject: {subject}", ln=True, align="L")
        
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return send_file(pdf_output, as_attachment=True, download_name="cover_letter.pdf", mimetype="application/pdf")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
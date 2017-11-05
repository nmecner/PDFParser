from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter #process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///pdf.db' #relative path for now
db = SQLAlchemy(app)


class Pdf(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.Text)
    info = db.Column(db.Text)

    def __init__(self, content, info):
        self.content = content
        self.info = info


def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text


currentpdf = Pdf(pdf_to_text('sample.pdf'), pdf_to_text('sample.pdf'))
db.create_all()
db.session.add(currentpdf)
db.session.commit()


@app.route('/')
def hello_world():
    return pdf_to_text('sample.pdf')


if __name__ == '__main__':
    app.run(debug=True)









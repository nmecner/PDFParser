from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter #process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
import xml.etree.ElementTree as ET
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/natalia/Projects/Parser/pdf.db' #reltive path for now
db = SQLAlchemy(app)


class Pdf(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.Text)
    info = db.Column(db.Text)

    def __init__(self, content, info):
        self.content = content
        self.info = info



db.create_all()


# Extracting information from xml parsed by PDFMiner

tree = ET.ElementTree(file='sam.xml')
root = tree.getroot()

textboxes = [] # list of textboxes
contents = [] # list of contents of textboxes
s = '' # string from one textbox


# get the coordinates of all the textboxes
for elm in root.getiterator(tag='textbox'):
    contents.append(s)
    s = ''
    textboxes.append((elm.tag, elm.attrib))
    for i in elm.getiterator(tag='text'):
        s += i.text


for i in range(len(textboxes)):
    db.session.add(Pdf((textboxes[i][1]['bbox']), contents[i]))


db.session.commit()

id = ''
all_ids = db.session.query(Pdf.id)
for i in all_ids:
    id += str(i)

con = db.session.query(Pdf.content)
pdf_text = ''
for t in con:
    pdf_text += str(t)
print(pdf_text)

pos = db.session.query(Pdf.info)
text_position = ''
for p in pos:
    text_position += str(p)
print(text_position)

@app.route('/')
def hello_world():
    return render_template('index.html', id=id, pdf_text=pdf_text, text_position=text_position)


if __name__ == '__main__':
    app.run(debug=True)









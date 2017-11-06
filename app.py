from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter #process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
import xml.etree.ElementTree as ET
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


db.create_all()


# Extracting information from xml parsed by PDFMiner

tree = ET.ElementTree(file='sample.xml')
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


# //display the data from database
@app.route('/')
def hello_world():
    return str(parsed_pdf_text)


if __name__ == '__main__':
    app.run(debug=True)









from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import xml.etree.ElementTree as ET
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdf.db'
db = SQLAlchemy(app)
admin = Admin(app)


class Pdf(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.Text)
    info = db.Column(db.Text)

    def __init__(self, content, info):
        self.content = content
        self.info = info


db.create_all()

admin.add_view(ModelView(Pdf, db.session))


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


#retrieving data and displaying them side by side in tabular form
id = ''
all_ids = db.session.query(Pdf.id)


@app.route('/')
def hello_world():
    results = db.session.query(Pdf)
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)









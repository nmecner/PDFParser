from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdfs.db' # realtive path for now
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

admin = Admin(app)


class Pdf(db.Model):
    txt = db.Column(db.VARCHAR, primary_key=True)


admin.add_view(ModelView(Pdf, db.session))

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)









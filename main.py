from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.sha256(b"somepasswordlol")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)


class URLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), unique=True)
    short = db.Column(db.String(255), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)


class URLForm(FlaskForm):
    original_url = StringField('Вставьте ссылку',
                               validators=[
                                   DataRequired(message='Ссылка не может быть пустой'),
                                   URL(message='Неверная сслыка')
                               ])
    submit = SubmitField('Получить короткую ссылку')


def get_short(original_url):
    h = hashlib.sha256(original_url.encode('utf-8'))
    return str(h.hexdigest())[:10]


# TODO: Home page
@app.route('/', methods=["POST", "GET"])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = URLModel()
        url.original_url = form.original_url.data
        url.short = get_short(form.original_url.data)
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('urls'))
    return render_template('index.html')


# TODO: Urls page
@app.route('/urls')
def urls():
    urls = URLModel.query.all()
    return render_template('urls.html', urls=urls[::-1])
    # pass


# TODO: Redirect page
@app.route('/<short>')
def url_redirect(short):
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(get_short("https://app.doma.uchi.ru/teacher/lessons"))
    app.run(debug=True)
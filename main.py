from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class CafeForm(FlaskForm):
    name = StringField(label='Cafe name', validators=[DataRequired()])
    map_url = StringField(label='Map Link', validators=[DataRequired(), URL()])
    img_url = StringField(label='Image Link', validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    seats = SelectField(label="Seats", choices=[('✔'), ('✖')])
    has_toilet = SelectField(label='Has Toilet', choices=[('✔'), ('✖')])
    has_wifi = SelectField(label="Has Wifi", choices=[('✔'), ('✖')])
    has_sockets = SelectField(label="Has Sockets", choices=[('✔'), ('✖')])
    can_take_calls = SelectField(label="Can take calls",choices=[('✔'), ('✖')])
    coffee_price = StringField(label='Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/cafes")
def cafes():
    cafes = db.session.query(Cafe).all()
    return render_template("cafes.html", list_of_cafes=cafes)

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return render_template('add.html', form=form)

    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

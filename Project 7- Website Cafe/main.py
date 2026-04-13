from flask import Flask, jsonify, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5

app= Flask(__name__)
bootstrap = Bootstrap5(app)
# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

app.config['SECRET_KEY']= 'jaijaijai'

with app.app_context():
    db.create_all()



class CafeForm(FlaskForm):
    name= StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    has_wifi = BooleanField('Wifi Available')
    coffee_price = StringField('Coffee Price')
    submit = SubmitField('Add Cafe')

class UpdatePriceForm(FlaskForm):
    coffee_price = StringField('Coffee Price')
    submit = SubmitField('Update Price')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template('cafes.html', cafes=all_cafes)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form= CafeForm()
    if form.validate_on_submit():
        new_cafe= Cafe(
            name= form.name.data,
            map_url= form.map_url.data,
            img_url= form.img_url.data,
            location= form.location.data,
            seats= form.seats.data,
            has_wifi=form.has_wifi.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash('Cafe added successfully!', 'success')
        return redirect(url_for('cafes'))
    return render_template('add.html', form= form)

@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe= db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash('Cafe deleted successfully!', 'danger')
    return redirect(url_for('cafes'))

@app.route('/update_price/<int:cafe_id>',methods=['GET', 'POST'])
def update_price(cafe_id):
    cafe= db.get_or_404(Cafe, cafe_id)
    form= UpdatePriceForm()
    if form.validate_on_submit():
        cafe.coffee_price= form.coffee_price.data
        db.session.commit()
        flash('Price updated successfully!', 'warning')
        return redirect(url_for('cafes'))
    return render_template('update_price.html', form=form, cafe= cafe)

@app.route('/search', methods= ['GET'])
def search_cafe():
    location= request.args.get('location')
    results= db.session.execute(db.select(Cafe).where(Cafe.location==location)).scalars().all()
    return render_template('search.html', cafes=results, location=location)

if __name__ == '__main__':
    app.run(debug=True)
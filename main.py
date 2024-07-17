import os
import random
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from forms import AddForm, UpdateForm, DeleteForm

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
bootstrap = Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record

@app.route("/random")
def get_cafe():
    cafe_data = db.session.execute(db.select(Cafe)).scalars()
    cafe_list = cafe_data.all()
    random_cafe = random.choice(cafe_list)
    cafe_list = [random_cafe]
    print(cafe_list)
    return render_template("cafes.html", cafes=cafe_list, heading="Random Cafe")


@app.route("/all")
def get_all_cafe():
    cafe_data = db.session.execute(db.select(Cafe)).scalars()
    cafe_list = cafe_data.all()
    # print(cafe_list)
    return render_template("cafes.html", cafes=cafe_list, heading="All Cafes")


@app.route("/find")
def find_cafe():
    loc = request.args.get("loc")
    selected_cafe = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalar()
    if not selected_cafe:
        return jsonify(error={"not found": "Sorry we couldn't find the cafe at that location."})
    else:
        return jsonify(cafe=selected_cafe.convert_to_dict())


# HTTP POST - Create Record
@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    add_form = AddForm()
    if add_form.validate_on_submit():
        new_cafe = Cafe(
            name=add_form.name.data,
            map_url=add_form.map_link.data,
            img_url=add_form.image_link.data,
            location=add_form.location.data,
            has_sockets=add_form.sockets.data,
            has_toilet=add_form.toilet.data,
            has_wifi=add_form.wi_fi.data,
            can_take_calls=add_form.calls.data,
            seats=add_form.seats.data,
            coffee_price=add_form.price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("get_all_cafe"))
    return render_template("add.html", form=add_form)


# HTTP PUT/PATCH - Update Record
@app.route("/update_price/<int:cafe_id>", methods=["GET", "POST"])
def update_price(cafe_id):
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        new_price = update_form.price.data
        cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return redirect(url_for("get_all_cafe"))
    return render_template("update.html", form=update_form)


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["GET", "POST"])
def delete_cafe(cafe_id):
    delete_form = DeleteForm()

    if request.method == "POST":
        api_key = delete_form.key.data
        cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()

        if api_key != "TopSecretAPIKey":
            return redirect(url_for("get_all_cafe"))

        if delete_form.validate_on_submit():
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return redirect(url_for("get_all_cafe"))

    return render_template("delete.html", form=delete_form)


if __name__ == '__main__':
    app.run(debug=True)

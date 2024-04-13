from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)

class Korisnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

class Dronovi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dron = db.Column(db.String, unique=True)

class Skupovi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skup = db.Column(db.String)        

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    messageKorisnik = db.session.query(Korisnik).all()
    messageDronovi = db.session.query(Dronovi).all()
    messageSkupovi = db.session.query(Skupovi).all()
    return render_template("index.html", messageKorisnik = messageKorisnik, messageDronovi=messageDronovi,messageSkupovi=messageSkupovi )


@app.route("/add-item", methods=["POST"])
def add_item():
    username = request.form.get("username")
    dron = request.form.get("dron")
    skup = request.form.get("skup")

    existing_dron = Dronovi.query.filter_by(dron=dron).first()

    if existing_dron:
        error_message = "Dron with that name already exists. Please enter a different name."
        # Render the template again with the error message
        messageKorisnik = db.session.query(Korisnik).all()
        messageDronovi = db.session.query(Dronovi).all()
        messageSkupovi = db.session.query(Skupovi).all()
        return render_template("index.html", messageKorisnik=messageKorisnik, messageDronovi=messageDronovi, messageSkupovi=messageSkupovi, error_message=error_message)
    else:
        korisnik = Korisnik(username=username)
        dronovi = Dronovi(dron=dron)
        skupovi = Skupovi(skup=skup)

        db.session.add(korisnik)
        db.session.add(dronovi)
        db.session.add(skupovi)
        db.session.commit()

        return redirect("/")

@app.route("/delete-korisnik", methods=["POST"])
def delete_korisnik():
    korisnik_id = request.form.get("korisnik_id")
    korisnik = Korisnik.query.get(korisnik_id)

    if korisnik:
        db.session.delete(korisnik)
        db.session.commit()

    return redirect("/")

@app.route("/delete-dron", methods=["POST"])
def delete_dron():
    dron_id = request.form.get("dron_id")
    dron = Dronovi.query.get(dron_id)

    if dron:
        db.session.delete(dron)
        db.session.commit()

    return redirect("/")

@app.route("/delete-skup", methods=["POST"])
def delete_skup():
    skup_id = request.form.get("skup_id")
    skup = Skupovi.query.get(skup_id)

    if skup:
        db.session.delete(skup)
        db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run() 

    
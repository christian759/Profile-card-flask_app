from flask import Flask, redirect, request, url_for, render_template
import model
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = '************'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model.db.init_app(app)

with app.app_context():
    model.db.create_all()


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/form/", methods=["POST", "GET"])
def form_page():
    error = None
    if request.method == "POST":
        photo = request.files.get('photo')
        photo_filename = None
        if photo and photo.filename != '':
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        person = model.Person(
            UserName=request.form['username'],
            Age=request.form['age'],
            Gender=request.form['gender'],
            Email=request.form['email'],
            Location=request.form['location'],
            About=request.form['about'],
            Photo=photo_filename
        )
        try:
            model.db.session.add(person)
            model.db.session.commit()
        except:
            error = "Username has already been used"
            
        return redirect(url_for("person", username=person.UserName))
    
    return render_template("form.html", error = error)


@app.route("/person/<username>")
def person(username):
    user = model.Person.query.filter_by(UserName=username).first_or_404()
    return render_template("user.html", user=user)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

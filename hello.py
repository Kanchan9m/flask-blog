from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
# add datebase
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/users'
app.config['SECRET_KEY'] = "my super key that no one supposed to know"
# app = Flask(__name__, template_folder='templatesaaa')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.app_context().push()

# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    fovorite_color = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Create a string
    def __repr__(self):
        return '<Name %r>' %self.name
    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete =  Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!!")
        our_users= Users.query.order_by(Users.date_added)
        
        return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)
    except:
        flash("Whoops! Try again..")
        return render_template("add_user.html",form=form,name=name,
        our_users=our_users)

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

#update
@app.route('/update/<int:id>', methods=['GET', "POST"])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Succesfully!")
            return render_template("update.html",
            form=form,
            name_to_update = name_to_update)
        except:
            flash("Error Try again..")
            return render_template("update.html",
            form=form,
            name_to_update = name_to_update)
    else:
        return render_template("update.html",
        form=form,
        name_to_update = name_to_update)

#Create a form class
class NamerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
# @app.route('/')
# def index():
#     return "<h1>Hello World!</h1>"

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User added seccessfully")
    our_users= Users.query.order_by(Users.date_added)
    print('abcd--------------------------------------------')
    print(our_users)
    
    return render_template("add_user.html",
    form=form,
    name=name,
    our_users=our_users)

@app.route('/')
def index():
    first_name = 'John'
    stuff = 'This is <strong>Bold</strong> Text'
    flash("Welcome to our website")
    pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", first_name=first_name,
        stuff=stuff,
        pizza=pizza)

# @app.route('/user/<name>')
# def user(name):
#     return "<h1>Hello.{}!</h1>".format(name)


@app.route('/user/<name>')
def user(name):

    return render_template("user.html",user_name=name)

#Create a error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    email = None
    form = NamerForm()
    form = NamerForm()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        email = form.email.data
        form.email.data = ''
        flash("Form Submitted Succsesfully!!")
    return render_template("name.html",
    name = name,
    email = email,
    form = form)


if __name__ == '__main__':
    app.run(debug=True)


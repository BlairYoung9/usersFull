from flask import Flask, render_template, request,redirect
from users import User  # Import Flask to allow us to create our app

app = Flask(__name__)    # Create a new instance of the Flask class called "app"

@app.route("/")
@app.route('/users')
def index():
    users = User.get_all()
    print(users)
    return render_template("users.html", users=users)

@app.route('/users/new', methods =["POST"])          # The "@" decorator associates this route with the function immediately following
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    id= User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect(f'/users/{id}')

@app.route('/users/add')
def add_user():
    return render_template("add_user.html")

@app.route('/users/<int:id>')
def show_user(id):
    users= User.get_one({'id' : id})
    return render_template("show_user.html", users=users)

@app.route("/users/<int:id>/edit")
def edit_user(id):
    users= User.get_one({'id' : id})
    return render_template("user_edit.html",users=users)

@app.route('/users/<int:id>/update', methods =['POST'])
def update_user(id):
    data = {
        **request.form,
        'id' : id
    }
    User.update_one(data)
    return redirect(f'/users/{id}')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    User.delete_one({'id' : id})
    return redirect('/')


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.

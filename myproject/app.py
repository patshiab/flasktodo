# created using tutorial from https://www.python-engineer.com/posts/flask-todo-app/

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()        #pushing application context

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#a todo item has an id, title, and complete status in the db
class Todo(db.Model):       #datastructure (table)
    id = db.Column(db.Integer, primary_key=True)    #parameter of table
    title = db.Column(db.String(100))       #parameter of table
    complete = db.Column(db.Boolean)        #parameter of table

#adds a todo item
@app.route("/add", methods=["POST"])        #routing
def add():
    title = request.form.get("title")       #variable
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))        #routing

#updates a todo item to complete or back to incomplete
@app.route("/update/<int:todo_id>")     #routing
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

#deletes a todo item
@app.route("/delete/<int:todo_id>")     #routing
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()     #variable   
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

#the home page
@app.route("/") 
def home():     #renders home page from template
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)        #template

if __name__ == "__main__":      #control flow
    db.create_all()     #creates initial db
    app.run(debug=True)
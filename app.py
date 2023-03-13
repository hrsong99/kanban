from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set up Flask and configure database file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)

# create a table called Tasks that takes in the id (the unique primary key), 
# column (to keep track of whether the task is in Todo, Doing, or Done),
# the content of the task itself, and the date created for ordering purposes
# As this is flask-sqlalchemy, the Base is db.Model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # overwrite representation as Task ID
        return '<Task %r>' % self.id

# Set app route when adding new tasks (POOST) or rendering kanban using current tasks (GET)
@app.route('/', methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST': # if posting new task to table:
        if "add_todo" in request.form: # if the request is from the form for adding todo tasks,
            task_content = request.form['add_todo'] # set task_content as the input from the form
            new_task = Tasks(content=task_content, column="Todo") # create a new task that takes the input as content and the column as Todo
        elif "add_doing" in request.form: # Do the same for the other columns
            task_content = request.form['add_doing']
            new_task = Tasks(content=task_content, column="Doing")
        else:
            task_content = request.form['add_done']
            new_task = Tasks(content=task_content, column="Done")

        try: # try adding the new task to the session and committing, before redirecting back to URL to update the page
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: # let user know there was an error if it doesn't work
            return 'Issue with adding task'

    else: # if the request method is not POST (i.e. it is GET)
        # select and separate the tasks based on which kanban column they belong to
        todo = Tasks.query.order_by(Tasks.date_created).where(Tasks.column=="Todo").all()
        doing = Tasks.query.order_by(Tasks.date_created).where(Tasks.column=="Doing").all()
        done = Tasks.query.order_by(Tasks.date_created).where(Tasks.column=="Done").all()
        # render the template using those three inputs (they are rendered using Jinja in index.html)
        return render_template('index.html', todo=todo, doing=doing, done=done)

# the app route when a task is deleted (i.e. when the delete url is submitted); 
# take the id of the deleted task as input for the function
@app.route('/delete/<int:id>')
def delete(id):
    # query the task based on the unique id of the task
    task_to_delete = Tasks.query.get_or_404(id)

    try: # try deleting the task from the sessoin before commiting and redirecting back to the page
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except: # raise an error if there is one
        return 'Problem deleting task'

# app route for moving a task from Todo or Done to Doing
@app.route('/to_doing/<int:id>', methods = ['GET','POST'])
def move_doing(id):
    # query the task based on id of task
    task_to_move = Tasks.query.get_or_404(id)

    try:
        # try changing the column value to Doing and then commiting & redirecting back
        task_to_move.column = "Doing"
        db.session.commit()
        return redirect('/')
    except: # raise an error if it doesn't work
        return 'Problem moving task'

# same as before, but for moving a task to the Done column
@app.route('/to_done/<int:id>', methods = ['GET','POST'])
def move_done(id):
    task_to_move = Tasks.query.get_or_404(id)

    try:
        task_to_move.column = "Done"
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem moving task'

# same as above, for moving a task to the Todo column
@app.route('/to_todo/<int:id>', methods = ['GET','POST'])
def move_todo(id):
    task_to_move = Tasks.query.get_or_404(id)

    try:
        task_to_move.column = "Todo"
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem deleting task'
# run the app when __name__ is "__main__" and set debug to True
if __name__ == "__main__":
    app.run(debug=True)
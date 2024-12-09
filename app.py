from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET', 'POST'])
def hello_world():

    if request.method == "POST":
        title =request.form['title']
        desc = request.form['desc']

        

        todo = Todo(title = title, desc = desc)
        db.session.add(todo)

        db.session.commit() #changes will be successfully commited

    allTodo = Todo.query.all()
    
    return render_template('index.html', allTodo = allTodo) #allTodo ko allTodo ke name se hi pass kiya

@app.route('/show')  # an endpoint
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is a product'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    
    # Handle case where `todo` is not found
    if not todo:
        return "Todo not found", 404
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        # Update the existing Todo
        todo.title = title
        todo.desc = desc
        db.session.commit()  # Save the changes to the database
        
        return redirect("/")  # Redirect to the home page
    
    # If accessed with GET, render the form with existing data
    return render_template('update.html', todo=todo)




@app.route('/delete/<int:sno>')  # an endpoint #delete route takes in a Serial Number
def delete(sno):#sno is the serial number passed to delete function
    todo = Todo.query.filter_by(sno=sno).first() #we used .first() because hamein woh pehla record hi delete karna hai
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/helloji')
def helloji():
    return render_template('index.html')

if __name__ == "__main__":
    # Use application context to create the database
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
    
    app.run(debug=True, port=8000)


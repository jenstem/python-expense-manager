from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mydatabase.db"))


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Expense(db.Model):
    """
    Model representing an expense record.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), unique=False, nullable=False)
    expensename = db.Column(db.String(80), unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)


@app.route('/')
def add():
    """
    Render the add expense form.
    """
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    """
    Delete an expense record by ID.
    """
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')


@app.route('/edit', methods=['POST'])
def edit():
    """
    Edit an existing expense record.
    """
    id = request.form['id']
    date = request.form['date']
    expensename = request.form['expensename']
    category = request.form['category']
    amount = request.form['amount']
    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.expensename = expensename
    expense.category = category
    expense.amount = amount
    db.session.commit()
    return redirect('/expenses')



@app.route('/updateexpense/<int:id>')
def updateexpense(id):
    """
    Render the update expense form for a specific expense.
    """
    expense = Expense.query.filter_by(id=id).first()
    return render_template('updateexpense.html', expense=expense)


@app.route('/expenses')
def expenses():
    """
    Display all expenses and their total amounts categorized.
    """
    expenses = Expense.query.all()
    total = 0
    t_food = 0
    t_shopping = 0
    t_transportation = 0
    t_entertainment = 0
    t_other = 0

    for expense in expenses:
        total += expense.amount
        if(expense.category == 'Food'):
            t_food += expense.amount
        elif(expense.category == 'Shopping'):
            t_shopping += expense.amount
        elif(expense.category == 'Transportation'):
            t_transportation += expense.amount
        elif(expense.category == 'Entertainment'):
            t_entertainment += expense.amount
        elif(expense.category == 'Other'):
            t_other += expense.amount
    return render_template('expenses.html', expenses=expenses, total=total, t_food=t_food, t_shopping=t_shopping, t_transportation=t_transportation, t_entertainment=t_entertainment, t_other=t_other)


@app.route('/addexpense', methods=['POST'])
def addexpense():
    """
    Add a new expense record to the database.
    """
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    expense = Expense(date=date, expensename=expensename, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect('/expenses')


if __name__ == '__main__':
    app.run(debug=True)

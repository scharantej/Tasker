 
# main.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    description = request.form.get('description')
    new_item = Todo(description=description, complete=False)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    item = Todo.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/mark_complete/<int:item_id>', methods=['POST'])
def mark_complete(item_id):
    item = Todo.query.get_or_404(item_id)
    item.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/get_items', methods=['GET'])
def get_items():
    items = Todo.query.all()
    return jsonify([{'id': item.id, 'description': item.description, 'complete': item.complete} for item in items])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

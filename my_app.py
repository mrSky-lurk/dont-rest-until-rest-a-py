from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


class MyDrink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(50))

    def __repr__(self):
        return f"ID: {self.id} -- Name: {self.name} -- Description: {self.desc}"


@app.route('/')
def index():
    return 'Hello - jello'


@app.route('/drinks')
def get_drinks():
    output = []
    param_id = request.args.get('id')
    if not param_id:
        drinks = MyDrink.query.all()
        for drink in drinks:
            drink_data = {'id': drink.id, 'Name': drink.name, 'Description': drink.desc}
            output.append(drink_data)
    else:
        drink = MyDrink.query.get_or_404(param_id)
        if not drink:
            return jsonify({'error_message': f'item not present with id {param_id}'}), 404
        drink_data = {'id': drink.id, 'Name': drink.name, 'Description': drink.desc}
        output.append(drink_data)
    return output


# @app.route('/drinks')
# def get_drink():
#     drink_data = MyDrink.query.get_or_404(id)
#     return jsonify({'id': id, 'Name': drink_data.name, 'Description': drink_data.desc}), 200


@app.route('/drinks/add', methods=['POST'])
def add_drink():
    name = request.json['name']
    desc = request.json['desc']
    with app.app_context():
        drink = MyDrink(name=name, desc=desc)
        db.session.add(drink)
        db.session.commit()
        return jsonify({"message": "drink addded"}), 201


@app.route('/drinks/del', methods=['POST', 'DELETE'])
def delete_drink():
    param_id = int(request.args.get('id'))
    del_drink = MyDrink.query.get_or_404(param_id)
    if not del_drink:
        return jsonify({'error_message': f'item not present with id {param_id}'}), 404
    db.session.delete(del_drink)
    db.session.commit()
    return jsonify({'status': 'DELETED_ITEM', 'id': del_drink.id, 'Name': del_drink.name, 'Description': del_drink.desc}), 201

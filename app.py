from flask import Flask, request, jsonify
import random
import string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unique_ids.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 10

db = SQLAlchemy(app)


class Id(db.Model):
    id = db.Column(db.String(20), primary_key=True)


def get_new_id(length):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        new_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=length))
        try:
            id = Id(id=new_id)
            db.session.add(id)
            db.session.commit()
            return new_id
        except:
            db.session.rollback()
        attempts += 1
    return None


@app.route('/generate-id', methods=['GET'])
def generate_id():
    id_length = 1
    while True:
        new_id = get_new_id(id_length)
        if new_id:
            return jsonify({'id': new_id})
        id_length += 1


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
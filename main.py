from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, func
app = Flask('app')
engine = create_engine('sqlite://')

metadata = MetaData()
cards = Table('cards', metadata,
  Column('id', Integer, primary_key=True),
  Column('title', String),
  Column('notes', String),
)
metadata.create_all(engine)

conn = engine.connect()
conn.execute(cards.insert(), [
  { 'title': 'Card 1', 'notes': 'Notes One' },
  { 'title': 'Card 2', 'notes': 'Notes Two' },
  { 'title': 'Card 3', 'notes': 'Notes Three' }
])

@app.route('/')
def hello_world():
  return jsonify({"name": 'Hello, World!'})

@app.route('/count')
def count_cards():
  rows = conn.execute(select([func.count(cards)])).scalar()
  return jsonify({"count": rows})

@app.route('/add_card',  methods=['POST'])
def add_card():
  data = request.get_json()
  result = conn.execute(cards.insert(), data)
  new_card_result = conn.execute(select([cards]).where(cards.c.id == result.lastrowid))
  new_card = new_card_result.fetchone()
  return jsonify({'id': new_card['id'], 'title': new_card['title'], 'notes': new_card['notes']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
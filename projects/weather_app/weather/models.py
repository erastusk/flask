from weather import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  cities = db.relationship('City', backref='user', lazy=True)

  def __repr__(self):
    return f"User('{self.email}', '{self.id}')" 

class City (db.Model):
  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(20), nullable=False) 
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"City('{self.city}', '{self.date_added}')" 
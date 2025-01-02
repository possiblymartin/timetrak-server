from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  def set_password(self, password):
    self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)

# Attendance Model
class Attendance(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  clock_in_time = db.Column(db.DateTime, nullable=False)
  clock_out_time = db.Column(db.DateTime, nullable=True)
  location = db.Column(db.String(100), nullable=False)
  is_late = db.Column(db.Boolean, default=False)
  reason_for_absence = db.Column(db.String(255), nullable=True)

  user = db.relationship('User', backref='attendance_records')

class WorkSchedule(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  work_start_time = db.Column(db.Time, nullable=False)
  work_end_time = db.Column(db.Time, nullable=False)

  user = db.relationship('User', backref='work_schedule')

class Holiday(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  holiday_date = db.Column(db.Date, unique=True, nullable=False)
  description = db.Column(db.String(100))

class UserPreferences(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  metric_name = db.Column(db.String(50), nullable=False)
  is_enabled = db.Column(db.Boolean, default=True)

  user = db.relationship('User', backref='preferences')
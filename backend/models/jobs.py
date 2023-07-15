from models.db import db
from datetime import datetime

class TOPJob(db.Model):
  __tablename__ = 'top_jobs'

  job_id = db.Column(db.Integer, primary_key=True)
  job_name = db.Column(db.String(100), nullable=True)
  job_description = db.Column(db.String(1000), nullable=True)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.String(100), nullable=True)  

  def __init__(self, job_name, job_description, user_id):
    self.job_name = job_name
    self.job_description = job_description
    self.user_id = user_id

  def __repr__(self):
    return f"<Action {self.job_name}>"
  
  def serialize(self):
    return {
      "job_id": self.job_id,
      "job_name": self.job_name,
      "job_description": self.job_description,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "user_id": self.user_id
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, job_name, job_description):
    self.job_name = job_name
    self.job_description = job_description
    self.updated_at = datetime.utcnow()
    db.session.commit()

  @classmethod
  def find_by_user_id(cls, user_id):
    return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

  @classmethod
  def find_by_id(cls, job_id):
    return cls.query.filter_by(job_id=job_id).first()
  
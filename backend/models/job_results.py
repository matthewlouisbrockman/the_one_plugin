from models.db import db
from datetime import datetime
import sqlalchemy.dialects.postgresql as postgresql


class TOPJobResult(db.Model):
  __tablename__ = 'top_job_results'

  result_id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=db.text("(uuid_generate_v4())"))
  parent_job_id = db.Column(db.Integer, nullable=False)
  result_data = db.Column(db.JSON, nullable=False, default={})
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.String(100), nullable=True)

  def __init__(self, parent_job_id, result_data, user_id):
    self.parent_job_id = parent_job_id
    self.result_data = result_data
    self.user_id = user_id

  def __repr__(self):
    return f"<Action {self.parent_job_id}>"
  
  def serialize(self):
    return {
      "result_id": self.result_id,
      "parent_job_id": self.parent_job_id,
      "result_data": self.result_data,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "user_id": self.user_id
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, parent_job_id, result_data):
    self.parent_job_id = parent_job_id
    self.result_data = result_data
    self.updated_at = datetime.utcnow()
    db.session.commit()

  @classmethod
  def find_results_for_job(cls, job_id, user_id):
    return cls.query.filter_by(parent_job_id=job_id, user_id=user_id).order_by(cls.created_at.desc()).all()
  
  @classmethod
  def find_by_id(cls, result_id):
    return cls.query.filter_by(result_id=result_id).first()



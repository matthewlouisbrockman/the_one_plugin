from flask_sqlalchemy import SQLAlchemy
# pip install flask_sqlalchemy

db = SQLAlchemy(
  engine_options={"pool_size": 20, "max_overflow": 0}
)

import json
from datetime import datetime
import uuid

def jsonify_payload(obj):
  return json.dumps(obj, cls=CustomJSONEncoder)

class CustomJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.isoformat()
    if isinstance(obj, uuid.UUID):
      return str(obj)
    return json.JSONEncoder.default(self, obj)
  

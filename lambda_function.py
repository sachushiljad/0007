from app import app
from serverless_wsgi import handle_request

def lambda_handler(event, context):
    return handle_request(app, event, context)
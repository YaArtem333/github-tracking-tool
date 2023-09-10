from app.app import app

@app.errorhandler(400)
def handle_bad_request(e):
    return {"error": "bad request"}, 400

@app.errorhandler(404)
def handle_not_found(e):
    return {"error": "page or resource not found"}, 404

@app.errorhandler(412)
def handle_precondition_failed(e):
    return {"error": "no such data in the database"}, 412

@app.errorhandler(415)
def handle_unsupported_media_type(e):
    return {"error": "unsupported media type"}, 415

@app.errorhandler(500)
def handle_server_error(e):
    return {"error": "some problems with server"}, 500


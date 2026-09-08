from flask import jsonify

class ApiResponse:

  def ok(message, data=None):
    response = {"message": message}
    
    if data is not None:
      response["data"] = data

    return jsonify(response), 200

  def created(message, data):
    return jsonify({"message": message, "data": data}), 201

  def bad_request(message):
    return jsonify({"message": message}), 400

  def not_found(message):
    return jsonify({"message": message}), 404
  
  def unauthorized(message):
    return jsonify({"message": message}), 401
  
  def conflict(message):
    return jsonify({"message": message}), 409
  
  def internal_server_error(message):
    return jsonify({"message": message}), 500
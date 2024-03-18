from flask import Blueprint, request, jsonify

# Create a new Flask Blueprint
keys = Blueprint('keys', __name__)

@keys.route('/register', methods=['PUT'])
def registerKey():
    req_json = request.json
    key_id = req_json.get("KeyID")
    if key_id:
        print(f"key id: {key_id}")
    
    return jsonify(success=True)

@keys.route('/set/color', methods=['POST'])
def setKeyColor():
    req_json = request.json
    key_idx = req_json.get("KeyIdx")
    color = req_json.get("Color")
    if key_idx:
        print(f"key id: {key_idx}")
    if color:
        print(f"color: {color}")
    
    return jsonify(success=True)
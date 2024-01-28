from flask import Blueprint, request, jsonify

# Create a new Flask Blueprint
key_input = Blueprint('key_input', __name__)

@key_input.route('/', methods=['GET'])
def home():
    return ('<h1>Key Input</h1>')

# set key buffer size, the underlying code will maintain a circular buffer of key inputs
@key_input.route('/size/<BufferSize>', methods=['PUT'])
def setBufferSize(BufferSize):
    return ('<h1>TODO: configure underlying circular buffer for key input</h1>')

# start reading keys
@key_input.route('/start', methods=['PUT'])
def start():
    return ('<h1>TODO: start reading keypresses to buffer</h1>')

# stop reading keys
@key_input.route('/stop', methods=['DELETE'])
def stop():
    return ('<h1>TODO: stop reading keypresses to buffer</h1>')

# pop key
@key_input.route('/pop', methods=['GET'])
def pop():
    fake_key_id = 32
    return fake_key_id

# pop all, can also be used to clear the buffer
@key_input.route('/pop/all', methods=['GET'])
def popAll():
    fake_keys = { "keys" : [ 32, 31, 33, 55 ] }
    return jsonify(fake_keys)
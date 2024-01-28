from flask import Blueprint, request, jsonify

# Create a new Flask Blueprint
conductor = Blueprint('conductor', __name__)

@conductor.route('/')
def home():
    return ('<h1>Conductor</h1>')

@conductor.route('/load/<MIDIFile>', methods=['PUT'])
def loadSong(MIDIFile):
    return ('<h1>TODO: load midi file from provided path</h1>')

@conductor.route('/song/info', methods=['GET'])
def getSongInfo():
    fake_song_info = { "length_seconds" : 155, "time_seconds": 15, "speed" : 1.5, "name" : "Don't Bring Me Down" }
    return jsonify(fake_song_info) # JSON w/ song length, time code, speed, name, etc

# set song time
@conductor.route('/song/time/<TimeSeconds>', methods=['POST'])
def setSongTime(TimeSeconds):
    return ('<h1>TODO: set the current time in the song</h1>')

# set song speed
@conductor.route('/song/time/<SpeedScalar>', methods=['POST'])
def setSongSpeed(SpeedScalar):
    return ('<h1>TODO: set the current speed of the song</h1>')

# pause
@conductor.route('/song/pause', methods=['POST'])
def pause():
    return ('<h1>TODO: pause the song</h1>')

# play
@conductor.route('/song/play', methods=['POST'])
def play():
    return ('<h1>TODO: play the song</h1>')


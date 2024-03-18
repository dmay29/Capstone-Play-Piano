from flask import Blueprint, request, jsonify

# Create a new Flask Blueprint
session_info = Blueprint("session_info", __name__)


@session_info.route("/mode", methods=["POST"])
def setMode():
    req_json = request.json
    mode = req_json.get("Mode")
    if mode:
        print(f"mode: {mode}")

    return jsonify(success=True)


@session_info.route("/mode", methods=["GET"])
def getMode():
    mode = "Learning"
    ret_dict = {"Mode": mode}
    return jsonify(ret_dict)


@session_info.route("/status", methods=["POST"])
def setStatus():
    req_json = request.json
    status = req_json.get("Status")
    if status:
        print(f"status: {status}")

    return jsonify(success=True)


@session_info.route("/status", methods=["GET"])
def getStatus():
    status = "Menu"
    ret_dict = {"Status": status}
    return jsonify(ret_dict)


@session_info.route("/sound/setting", methods=["POST"])
def setSoundSetting():
    req_json = request.json
    sound_setting = req_json.get("SoundSetting")
    if sound_setting:
        print(f"sound_setting: {sound_setting}")

    return jsonify(success=True)


@session_info.route("/sound/setting", methods=["GET"])
def getSoundSetting():
    sound_setting = "Grand"
    ret_dict = {"SoundSetting": sound_setting}
    return jsonify(ret_dict)


@session_info.route("/speed", methods=["POST"])
def setSpeed():
    req_json = request.json
    speed = req_json.get("Speed")
    if speed:
        print(f"speed: {speed}")

    return jsonify(success=True)


@session_info.route("/speed", methods=["GET"])
def getSpeed():
    speed = 1.5
    ret_dict = {"Speed": speed}
    return jsonify(ret_dict)


@session_info.route("/song/name", methods=["POST"])
def setSongName():
    req_json = request.json
    song_name = req_json.get("SongName")
    if song_name:
        print(f"song_name: {song_name}")

    return jsonify(success=True)


@session_info.route("/song/name", methods=["GET"])
def getSongName():
    song_name = "Mary Had a Little Lamb"
    ret_dict = {"SongName": song_name}
    return jsonify(ret_dict)

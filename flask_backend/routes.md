# Flask Route HTTP Endpoints

## Register a key
Registers a key of interest with the backend, the backend will report to the frontend when this key is press/changed
 - Route: `/k/register`
 - HTTP Verb: `PUT`
 - Input: `{ "KeyID": String }`

## Set key color
Sets the color of a key, the device should be in menu mode, this may be enforced by the backend
 - Route: `/k/set/color`
 - HTTP Verb `POST`
 - Input: `{ "KeyIdx": int, "Color": [ uint8, uint8, uint8 ]}`

## Set/Get Mode
Sets or gets the current game mode
 - Route: `/si/mode`
 - HTTP Verb `POST`, `GET`
 - Input/Output: `{ "Mode": String }`

## Set/Get Status
Sets or gets the current status, playing, paused, menu, etc
 - Route: `/si/status`
 - HTTP Verb `POST`, `GET`
 - Input/Output: `{ "Status": String }`

## Set/Get Sound Setting
Set or get the current sound setting which alters the piano sound ex. Grand, Organ
 - Route: `/si/sound/setting`
 - HTTP Verb `POST`, `GET`
 - Input/Output: `{ "SoundSetting": String }`

## Set/Get Speed
Sets or gets the songs speed/tempo a floating point number that is used to scale the song speed
 - Route: `/si/speed`
 - HTTP Verb `POST`, `GET`
 - Input/Output: `{ "Speed": Float }`

## Set/Get Song Name
desc
 - Route: `/si/song/name`
 - HTTP Verb `POST`, `GET`
 - Input/Output: `{ "SongName": String }`
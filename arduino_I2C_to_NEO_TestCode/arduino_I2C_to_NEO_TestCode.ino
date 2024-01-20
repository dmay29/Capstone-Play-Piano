/*
  Allows Arduino MEGA to on-load and process song data sent by Raspberry PI, 
    then play song when asked to execute. Can store a minimum of a 5 minute song.

  TO UPLOAD AND PROCESS SONG:
    - Send MIDI data over I2C
        MESSAGE FORM: 
            1) Begin by sending a string "Start PreloadXX" over I2C
            2) Then send a string line of 62 values, representing keys 0-61 and the timestamp in the form:
                - each key is represented by either a 0 or 1 to show if the key is turned on
                - each value is seperated by a single space
                - the timestamp is the final value
                - after each line/timestamp, end the line with 'XX'
              EXAMPLE: "Start PreloadXX[61 zeroes or ones seperated by a space]*space*[timestamp]XX...
                                      [61 zeroes or ones seperated by a space]*space*[timestamp1]XX...
                                      [61 zeroes or ones seperated by a space]*space*[last-timestamp]XX
                        End PreloadXX"
            3) End song transfer by sending string "End PreloadXX" over I2C
            4) Arduino will save and process the data to create a cascading note effect

  TO BEGIN LEARNING/PLAY-ALONG SONG:
    - Send a string "Start SongXX [time-scale * 10]XX" over I2C
      1) For example a song at regular speed would require: "Start SongXX 10XX"
      2) Half-speed would require: "Start SongXX 5XX"
      3) Double-speed would require: "Start SongXX 20XX"

  TO BEGIN Freeplay:
    - Send a string "Free PlayXX" over I2C
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

//random i2c vals
#define NanoI2C_Left 8        //controls the LED matrix of the left most 3 octaves (30 keys)
#define NanoI2C_Right 10      //controls the LED matrix of the right most 3 octaves and highest C (31 keys)
#define GIGA_I2C 6            //controls the LED matrix of 5 octaves (4 12-key and 1 13-key)

//NEOPixels strips controlled by NanoI2C_Left
#define Octave_1 D3
#define Octave_2 D6
#define Octave_3 D9

//NEOPixels strips controlled by NanoI2C_Right
#define Octave_4 D3
#define Octave_5_plus1 D6

const int Max_Timestamps = 6000; // Example maximum number of timestamps
int8_t Song_Data[Max_Timestamps][61]; // 63 by Max_Timestamp data structure [index, binary for Notes 0-61, timestamp]
uint16_t Song_Data_Timestamp[Max_Timestamps];

//create definitions for MATRIX values for each midi key, and their tails

//convert the recieved notes to a timestamped array of all notes and their tails (have var for tail duration) (have a time scale option)

//create function to cycle through row, wait for timestamp, and execute

//create a recieve event for beginning the song, this should also send the time scale 

int row_Index = 0;
bool is_Preloading = false;
String I2C_Buffer = "";

void setup() {
    Wire.begin(GIGA_I2C); // Join I2C bus with address #8
    Wire.onReceive(receiveEvent); // Register receive event
    Serial.begin(9600); // Start serial communication for debugging
}

void loop() {
  int Rows_to_Print = 50;
  printFirstXRows(Rows_to_Print);
}

void receiveEvent(int howMany) {
    while (Wire.available()) {
        char c = Wire.read();
        if (c == 'XX') {
            processBuffer();
            I2C_Buffer = ""; // Clear buffer for next line
        } else {
            I2C_Buffer += c; // Append character to buffer
        }
    }
}

void processBuffer() {
    if (I2C_Buffer == "Start PreloadXX") {
        is_Preloading = true;
        row_Index = 0;
    } 
    else if (I2C_Buffer == "End PreloadXX") {
        is_Preloading = false;
        //song is stored
    } 
    else if (is_Preloading) {
        parseAndStoreData(I2C_Buffer);
    }
    else if (I2C_Buffer == "Start SongXX") {
        startLearning();
    }    
    else if (I2C_Buffer == "Free PlayXX") {
        freePlayMode();
    }
}

void parseAndStoreData(String data) {
    if (data.endsWith("XX")) {
        data.remove(data.length() - 2); // Remove "XX"

        int spaceIndex;
        int column = 0; 
        // Loop to process 62 notes
        for (int i = 0; i < 61; ++i) {
            spaceIndex = data.indexOf(' ');
            if (spaceIndex == -1) {
                // Handle error: fewer than 62 notes in the data
                Serial.println("Error: insufficient note data");
                return;
            }

            String noteString = data.substring(0, spaceIndex);
            int note = noteString.toInt();
            Song_Data[row_Index][column] = note;
            data = data.substring(spaceIndex + 1); // Move to the next part of the data string
            column++;
        }
        // Process the timestamp, which is now the remainder of the string
        Song_Data_Timestamp[row_Index] = (uint16_t) data.toInt();
        row_Index++; // Move to the next row
    }
}

void printFirstXRows(int x) {
    for (int i = 0; i < x; i++) { // Loop through the first 50 rows
        for (int j = 0; j < 61; j++) { // Loop through each column in the row
            Serial.print(Song_Data[i][j]);
            Serial.print(" "); // Print a space between columns
        }
        Serial.println(); // Print a newline at the end of each row
    }
}

void startLearning(){

}

void freePlayMode(){

}
/*
 *  HTTP POST request to WEB SERVER PRODUCER ESP
 *
 *  This module sends a json formatted string in to
 *  the web server containing the data sensed from
 *  its input pins
 *  
 */

//HTTP headers
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>

//JSON formatter header 
//https://bblanchon.github.io/ArduinoJson/
#include <ArduinoJson.h>

//TODO: put the pin initializers here
//int pinOut8 = 8;
//int pinOut7 = 7;
//int pinOut6 = 6;
//int pinOut5 = 5;
int pinOut4 = D4;
int pinInA0 = A0;
int valueInA0 = 0;

String ESPID = "MCU-P1";

//setup variables and WIFI connection
void setup() {

  //TODO: setup pin configurations
//  pinMode(pinOut8, OUTPUT);                    // Setting Pin 8 as output
//  pinMode(pinOut7, OUTPUT);                    // Setting Pin 7 as output
  pinMode(pinOut4, OUTPUT);                    // Setting Pin 6 as output
  pinMode(pinInA0, INPUT);                     // Setting analog pin A0 to input

//  digitalWrite(pinOut8, LOW);
//  digitalWrite(pinOut7, LOW);
//  digitalWrite(pinOut6, LOW);
//  digitalWrite(pinOut5, LOW);
  
  //Serial connection
  Serial.begin(9600);
    
  //WiFi connection
  WiFi.begin("Globehack2017", "Hackathon2017");     

  //Wait for the WiFI connection completion
  while (WiFi.status() != WL_CONNECTED) {  
    delay(500);
    Serial.println("Waiting for connection");
  }
}
 
void loop() {

 //Check WiFi connection status
 if(WiFi.status()== WL_CONNECTED){            

//    digitalWrite(pinOut8, HIGH);
    float v_consumption = analogRead(pinInA0) * 3.3/1023.0;
    delay(300);
    Serial.println(v_consumption);
//    digitalWrite(pinOut8, LOW);
//    digitalWrite(pinOut7, HIGH);
    float i_consumption = analogRead(pinInA0);
    delay(300);

//    digitalWrite(pinOut8, LOW);
//    digitalWrite(pinOut7, LOW);
//    digitalWrite(pinOut6, HIGH);
    float v_distribution = analogRead(pinInA0) * 3.3/1023.0;
    delay(300);

//    digitalWrite(pinOut8, LOW);
//    digitalWrite(pinOut7, LOW);
//    digitalWrite(pinOut6, LOW);
//    digitalWrite(pinOut5, HIGH);
    float i_distribution = analogRead(pinInA0);
    delay(300);    
      
    // Memory pool for JSON object tree.
    //
    // Inside the brackets, 500 is the size of the pool in bytes.
    // If the JSON object is more complex, you need to increase that value.
    StaticJsonBuffer<500> jsonBuffer;

    // Create the root of the object tree.
    //
    // It's a reference to the JsonObject, the actual bytes are inside the
    // JsonBuffer with all the other nodes of the object tree.
    // Memory is freed when jsonBuffer goes out of scope.
    JsonObject& root = jsonBuffer.createObject();    

    // Add a nested object.
    JsonObject& consumption = root.createNestedObject("consumption");
    JsonObject& distribution = root.createNestedObject("distribution");

    root["espid"] = ESPID;
    consumption["voltage"] = v_consumption; // 1
    consumption["current"] = i_consumption; // 1

    distribution["voltage"] = v_distribution; // 1
    distribution["current"] = i_distribution; // 1
  
    // Add values in the object
    //
    // Most of the time, you can rely on the implicit casts.
    // In other case, you can do root.set<long>("time", 1351824120);
    root["switch"] = false; // false

    //JSON output
    //  {
    //  "espid: 1,
    //  "consumption": {
    //      "voltage": 1,
    //      "current": 1
    //  },
    //  "distribution": {
    //      "voltage": 1,
    //      "current:": 1
    //  },
    //  "branch1": false,
    //  "branch2": false,
    //  "branch3": false,
    //  "branch4": true,
    //  "timestamp": "timestamp"
    //}

    String data;

    //print JSON to data
    root.printTo(data);

    //Declare object of class HTTPClient
    HTTPClient http;

    //Specify request destination
    http.begin("http://inteliqas-kelvin-abella.c9users.io:8080/esprequestproducer");

    //Specify content-type header
    http.addHeader("Content-Type", "application/json");

    //Send the request
    int httpCode = http.POST(data);

    //Get the response payload
    String payload = http.getString();
    
    //Print HTTP return code
    Serial.println(httpCode);
    
    //Print request response payload
    Serial.println(payload);

    StaticJsonBuffer<500> jsonBufferRead;

    JsonObject& rootRead = jsonBufferRead.parseObject(payload);
    
    if (!rootRead.success())
    {
      Serial.println("parseObject() failed");
    }
    String esp_id = rootRead["espid"];
    int switch_j = rootRead["switch"];

    if (switch_j == 1) {
      digitalWrite(pinOut4, HIGH);
    } else {
      digitalWrite(pinOut4, LOW);
    }
    
    if (esp_id == ESPID) {
      bool branch1Read = rootRead["branch1"];
      bool branch2Read = rootRead["branch2"];
      bool branch3Read = rootRead["branch3"];
      bool branch4Read = rootRead["branch4"];

      if (branch4Read == true) {
//        digitalWrite(pinOut4, HIGH);
      }
      if (branch3Read == true) {
//        digitalWrite(pinOut3, HIGH);
      }
      if (branch2Read == true) {    
//        digitalWrite(pinOut2, HIGH);
      }
      if (branch1Read == true) {
//        digitalWrite(pinOut1, HIGH);
      }
    }

    
    //Close connection
    http.end();
 
 }else{
    //throw error in connection
    Serial.println("Error in WiFi connection");
 }
  //Send a request every 5 seconds
  delay(100);
}
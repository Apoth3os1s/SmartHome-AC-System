//This includes the library which has the code to calculate and measure the temperature and humididty
#include "Adafruit_DHT.h"
//This deifines which pin the data will come from, from the DHT22 temp and humidity sensor
#define DHTPIN 2
//Defines which type of sensor I will be using
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
//////////////////////////////////////////////////////
void setup() 
{
	dht.begin();
	float temp; // creates a variable of float for temp as the temp reading contains decimalas
}
//////////////////////////////////////////////////////
void loop() 
{
// Waits 30 secounds before runnning the code again
	delay(500);
    float temp = 0;
// Reads temperature as Celsius
    while (temp < 5.0 || temp > 50){ // Checks to see if the temp reading is realistic if not it tries to collect again until it does
        temp = dht.getTempCelcius();
    }
//Uploads the value to the webhook
    if (temp > 5.0 && temp < 50){ // Checks to see if the values that it has been passed are within a realistic range if not it does not send the value.
        Particle.publish("temp", String(temp), PRIVATE);          // I added the second check as a fail safe as I somehow kept recieving 0 values 
        delay(1500);
    }
}
//////////////////////////////////////////////////////

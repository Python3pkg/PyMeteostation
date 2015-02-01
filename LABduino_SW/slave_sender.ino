#include <Wire.h>

#define I2C_ADDRESS 0x04
#define WIND_DIR_PIN 0
#define WIND_DIR_THRESHOLD 20
#define LED_PIN 13

int wind_dir = 0;
int wind_table[] = {27, 61, 106, 332, 802, 680, 511, 202};

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(dataRequest);
}

void loop() {
  digitalWrite(LED_PIN, LOW);
  wind_dir = wind_direction();
  digitalWrite(LED_PIN, HIGH);
  delay(500);
}

int wind_direction() {
  int x = analogRead(WIND_DIR_PIN);
  for(int i=0;i<8;i++){
    if((wind_table[i]-WIND_DIR_THRESHOLD < x) and (x < wind_table[i]+WIND_DIR_THRESHOLD)){
      return(i);
    }
  }
  return(wind_dir);
}

void dataRequest(){
 byte i2c[] = {wind_dir};
 Wire.write(i2c,sizeof(i2c));
}

// This code interfaces with a python script to control three color
// channels of LED lighting according to the cheerlights api

int machinestate = 0;

int red = 9;
int green = 10;
int blue = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  int ch; 
  if (Serial.available() > 0) {
    ch = Serial.read();
    switch (machinestate) {
      case 0:
        if (ch == 0xAA) machinestate = 1;
      break;
      case 1:
        if (ch == 0x55) {
          machinestate = 2;
        }
        else {
          machinestate = 0;
        }
      break;
      case 2:
        if (ch == 0xAA) {
          machinestate = 3;
        }
        else {
          machinestate = 0;
        }
      break;
      case 3:
        analogWrite(red, ch);
        machinestate = 4;
      break;
      case 4:
        analogWrite(green, ch);
        machinestate = 5;
      break;
      case 5:
        analogWrite(blue, ch);
        machinestate = 0;
      break;
    }
  }
}

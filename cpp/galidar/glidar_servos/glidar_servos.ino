#include <Servo.h>

Servo servoX;
Servo servoY;

bool start = false;
int incomingByte = 0; // For incoming serial data

int xpos = 90; // Starting yaw angle
int ypos = 45; // Starting pitch angle
int degrees = 180; // Amount to rotate

int scanNum = 0;  // Lines scanned

int scanLimit = 10; // Lines to scan
int delayTime = 100; // Time between servo position change
int incrementX = 2; // Amount to move x servo
int incrementY = 10; // Amount to move y servo

void setup() {
  Serial.begin(115200);
  while (!Serial);
}

void servoRtoL() {
  Serial.print(xpos);
  Serial.print("\t");
  Serial.println(ypos);

  xpos = xpos + incrementX;

  servoX.attach(9);
  servoX.write(xpos);
  delay(delayTime); // Wait to complete movement
}

void servoLtoR() {
  Serial.print(xpos);
  Serial.print("\t");
  Serial.println(ypos);

  xpos = xpos - incrementX;

  servoX.write(xpos);
  delay(delayTime); // Wait to complete movement
}

void runServos() {
  if (start) {
  
  servoX.attach(9);
  servoY.attach(10);
  
  servoX.write(xpos); // Set initial position
  servoY.write(ypos); // Set initial position
  
  delay(delayTime); // Wait to complete movement
  
  if (scanNum <= scanLimit) {
    for (xpos = 0; xpos <= degrees; xpos += incrementX) {
      servoRtoL();
    }

    ypos = ypos + incrementY; // Move Y when end of row reached
    servoY.write(ypos);

    delay(delayTime); // Wait to complete movement

    scanNum = scanNum + 1;

    for (xpos = degrees; xpos >= 0; xpos -= incrementX) {
      servoLtoR();
    }

    ypos = ypos + incrementY; // Move Y when end of row reached
    scanNum = scanNum + 1;
    servoY.write(ypos);
  
    delay(delayTime); // Wait to complete movement

    if (scanNum >= scanLimit) {
      endScan();
    }
  }
  }
}

void endScan() {
  servoX.write(90);  // Reset servos
  servoY.write(90);
  delay(delayTime); // Wait to complete movement
  servoX.detach();
  servoY.detach();
  Serial.println("000");
  start = false;
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read(); // wait to start
    start = true;
  }
  runServos();
}

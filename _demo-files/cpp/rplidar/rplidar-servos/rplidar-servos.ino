/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>
#include <Async_Operations.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int minAngle = 0;
int maxAngle = 180;
bool runServo = true;
int delayTime = 500;  // how long to pause at each angle

long long dt[] = {delayTime};
Async_Operations delayed(dt, 1, 1000);

void setup() {
  Serial.begin(1200);
  // pinMode(LED_BUILTIN, OUTPUT);
  delayed.setLoopCallback(&run);
  delayed.start();
  myservo.attach(10);
}

void test() {
  myservo.write(180);
  Serial.println(pos);
  delay(delayTime);
}

void run() {
    if (pos < 180) {
      pos += 2;
      myservo.write(pos);
      Serial.println(pos);
  } 
      if (pos >= 180) {
      myservo.write(90);
      delay(140); 
      myservo.detach();
      runServo = false;
      Serial.println("000");
    } 
}

void loop() {
  // test();
  delayed.update();
  Serial.println(pos);
}
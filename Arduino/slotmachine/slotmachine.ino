const int ON = LOW;
const int OFF = HIGH;

const int leftPin = 4;
const int centerPin = 5;
const int rightPin = 6;
const int startPin = 3;

void setup() {
  Serial.begin(9600);
  pinMode(leftPin,INPUT_PULLUP);
  pinMode(centerPin,INPUT_PULLUP);
  pinMode(rightPin,INPUT_PULLUP);
  pinMode(startPin,INPUT_PULLUP);
}

void loop() {
  if (digitalRead(leftPin) == ON){
    Serial.println("left");
  }else if (digitalRead(centerPin) == ON){
    Serial.println("center");
  }else if (digitalRead(rightPin) == ON){
    Serial.println("right");
  }else if (digitalRead(startPin) == ON){
    Serial.println("start");
  }
  else{
    Serial.println("");
  }
  Serial.flush();
  //delay(40);
}

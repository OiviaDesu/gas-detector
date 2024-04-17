// GAS DETECTOR

#define INPUT_PIN A0
#define RED_LED_PIN 2
#define GREEN_LED_PIN 3
#define BUZZER_PIN 4
#define THRESHOLD 400

int is_leak = 0;

// Value read from the gas sensor
unsigned long sensor_val;

void setup() {
  Serial.begin(9600);
  
  // Initialize the input and output pins
  pinMode(INPUT_PIN, INPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // Read the value from the gas sensor
  sensor_val = analogRead(INPUT_PIN);
  is_leak = sensor_val >= THRESHOLD;

  // Setting the led and the buzzer according to 
  // is the gas leak or not
  digitalWrite(RED_LED_PIN, is_leak);
  digitalWrite(GREEN_LED_PIN, !is_leak);
  digitalWrite(BUZZER_PIN, is_leak);

  // print out the value of the sesnor and
  // the state of gas leak in one line
  // separate by a space
  Serial.print(sensor_val);
  Serial.print(" ");
  Serial.println(is_leak);

  // check every 3s
  delay(3 * 1000);
}

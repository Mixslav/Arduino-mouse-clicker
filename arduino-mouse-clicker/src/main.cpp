#include <Arduino.h>

const uint8_t SWITCH_PIN = 2;
const unsigned long LOCKOUT_MS = 8;
const unsigned long LED_MS = 30;
const unsigned long HEARTBEAT_MS = 5;
const uint8_t CLICK_PAD = 63;  // pad 'C' to a full 64-byte USB packet to force flush

static int lastStableState = HIGH;
static unsigned long lockoutUntil = 0;
static unsigned long ledOffAt = 0;
static unsigned long lastBeat = 0;
static bool ledOn = false;

void setup() {
  pinMode(SWITCH_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  if (ledOn && now >= ledOffAt) {
    digitalWrite(LED_BUILTIN, LOW);
    ledOn = false;
  }

  if (now - lastBeat >= HEARTBEAT_MS) {
    Serial.write('.');
    lastBeat = now;
  }

  if (now < lockoutUntil) return;

  int reading = digitalRead(SWITCH_PIN);
  if (reading != lastStableState) {
    if (reading == LOW) {
      Serial.write('C');
      for (uint8_t i = 0; i < CLICK_PAD; i++) Serial.write('.');
      Serial.flush();
      digitalWrite(LED_BUILTIN, HIGH);
      ledOn = true;
      ledOffAt = now + LED_MS;
      lastBeat = now;
    }
    lastStableState = reading;
    lockoutUntil = now + LOCKOUT_MS;
  }
}

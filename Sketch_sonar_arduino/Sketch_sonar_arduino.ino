#include <Ultrasonic.h>

#define TRIGGER_PIN  12
#define ECHO_PIN     13
Ultrasonic ultrasonic(TRIGGER_PIN, ECHO_PIN);
void setup()
  {
  Serial.begin(9600);
  }
unsigned long int tempoAtual = 0;
unsigned long tempoFinal = 0;
unsigned long cronometro = 0;
void loop()
  {
  
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
    cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
    inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);
  //Intervalo entre Trigger e Echo
  Serial.print(microsec);
  //Distancia convertida em cm e mm
  Serial.print(",");
  Serial.print(cmMsec);
  Serial.print(",");
  //tempo no cronometro
  cronometro = millis();
  Serial.println(cronometro);
  delay(50);
  }

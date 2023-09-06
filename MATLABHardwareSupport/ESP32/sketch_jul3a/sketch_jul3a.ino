#include <WiFi.h>
#include <analogWrite.h>

WiFiServer server(1234);  // Define el objeto del servidor en el puerto 1234

const char* ssid = "fh_6625b0";      // Nombre de la red Wi-Fi
const char* password = "wlan99da4f";  // Contraseña de la red Wi-Fi

#define ain1  16
#define ain2  27
#define pwm_a  17

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  pinMode(ain1, OUTPUT); 
  pinMode(ain2, OUTPUT); 


  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  Serial.println("Conexión WiFi establecida");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
  server.begin();  // Inicia el servidor
  Serial.println("Servidor iniciado");
}


void loop() {
  WiFiClient client = server.available();  // Espera a que se conecte un cliente
  if (client) {
    Serial.println("Cliente conectado");
    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');  // Lee el comando enviado por el cliente
        command.trim();  // Elimina espacios en blanco al inicio y al final
        Serial.print("Comando recibido: ");
        Serial.println(command);
        
        // Aquí puedes agregar tu lógica para procesar el comando recibido

        client.println("Comando recibido: " + command);  // Envía una respuesta al cliente

         if (command == "codigo1") {
          // Lógica para ejecutar el código 1
          // Aquí puedes agregar el código que deseas ejecutar de forma remota
          analogWriteFrequency(500);
          digitalWrite(ain1, HIGH); 
          digitalWrite(ain2, LOW);
          analogWrite(pwm_a, 50); 
          delay(1000);
          analogWrite(pwm_a, 0); 
        } 
      }
    }
    client.stop();  // Cierra la conexión con el cliente
    Serial.println("Cliente desconectado");
  }
}
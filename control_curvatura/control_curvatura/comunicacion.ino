void udp_recep() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // receive incoming UDP packets
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
    int len = udp.read(paquete_entrante, 64);
    if (len > 0) {
      paquete_entrante[len] = 0;
    }
    //Serial.printf("UDP packet contents: %s\n", paquete_entrante);
    if (paquete_entrante[0] == 'L') {                //SOLICITUDE DE ESTADO
      //Serial.println("LECTURA");
      lectura_estado(len);
    }
    else if (paquete_entrante[0] == 'E') {          //ESCRITURA DE PARAMETROS
      //Serial.println("ESCRITURA");
      //Serial.println(configuracion_remota(len));
      cadena = configuracion_remota(len);
      cadena.toCharArray(msg, cadena.length() + 1);
      udp.beginPacket(udp.remoteIP(), udp.remotePort());
      udp.printf(msg);
      udp.endPacket();
    }
    else if (paquete_entrante[0] == 'V') {          //RECEPCION DE DATOS PREDECESOR
      //Serial.println("DatosPREDECESOR");
      estado_predecesor(len);
    }
  }
}
void lectura_estado(int len) {
  String mensaje;
  for (int i = 1; i < len; i++) {
    char nuevo = paquete_entrante[i];
    mensaje.concat(nuevo);
  }
  if (mensaje == "/estado_predecesor") {
    cadena = "V/" + parar + "/" + String(Input_vel) + "/" + String(vel_ref) + "/" + String(curvatura_predecesor);
  }
  else {
    cadena = "incorrecto";
  }
  cadena.toCharArray(msg, cadena.length() + 1);
  for (int i = 0; i < 3; i++) {
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.printf(msg);
    udp.endPacket();
  }
}

String configuracion_remota(int len) {
  String variable;
  int i = 1;
  while ((paquete_entrante[i] != '/' || i == 1) && i < len) {
    char nuevo = paquete_entrante[i];
    variable.concat(nuevo);
    i++;
  }
  String dato;
  int j = i + 1;
  while (i < len - 1) {
    char nuevo = paquete_entrante[i + 1];
    dato.concat(nuevo);
    i++;
  }
  //Serial.println(variable);
  //Serial.println(dato);
  //Serial.println(j);
  //Serial.println(paquete_entrante[j]);
  //Serial.println(dato.toFloat());
  //Serial.println(len);
  if ((dato.toFloat() == 0 && (j < len && paquete_entrante[j] != '0')) && variable != "/parar") {
    return "datoIncorrecto";
  }
  if (variable == "/co_p") {
    Kp_theta = dato.toFloat();
    //PID_theta.SetTunings(Kp_theta, Ki_theta, Kd_theta);
  }
  else if (variable == "/co_i") {
    Ki_theta = dato.toFloat();
    //PID_theta.SetTunings(Kp_theta, Ki_theta, Kd_theta);
  }
  else if (variable == "/co_d") {
    Kd_theta = dato.toFloat();
    //PID_theta.SetTunings(Kp_theta, Ki_theta, Kd_theta);
  }
  else if (variable == "/cv_p") {
    Kp_vel = dato.toFloat();
    //PID_vel.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cv_i") {
    Ki_vel = dato.toFloat();
    //PID_vel.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cv_d") {
    Kd_vel = dato.toFloat();
    //PID_vel.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cv_ref") {
    sp_vel = dato.toFloat();
  }
  else if (variable == "/cd_p") {
    Kp_d = dato.toFloat();
    //PID_d.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cd_i") {
    Ki_d = dato.toFloat();
    //PID_d.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cd_d") {
    Kd_d = dato.toFloat();
    //PID_d.SetTunings(Kp_vel, Ki_vel, Kd_vel);
  }
  else if (variable == "/cd_delta") {
    delta = dato.toFloat();
  }
  else if (variable == "/cd_ref") {
    d_ref = dato.toFloat();
  }
  else if (variable == "/calibrar") {
    calibrar = dato.toFloat();
  }
  else if (variable == "/parar") {
    parar = dato;
  }
  else {
    return "incorrecto";
  }
  return "ok";
}

void estado_predecesor(int len) {
  String PARAR;
  int i = 2;
  while (paquete_entrante[i] != '/' && i < len) {
    char nuevo = paquete_entrante[i];
    PARAR.concat(nuevo);
    i++;
  }
  String VEL;
  int j = i + 1;
  i++;
  while (paquete_entrante[i] != '/' && i < len) {
    char nuevo = paquete_entrante[i];
    VEL.concat(nuevo);
    i++;
  }
  String refVel;
  int k = i + 1;
  i++;
  while (paquete_entrante[i] != '/' && i < len) {
    char nuevo = paquete_entrante[i];
    refVel.concat(nuevo);
    i++;
  }
  String CURVA_predecesor;
  int m = i + 1;
  while (i < len - 1) {
    char nuevo = paquete_entrante[i + 1];
    CURVA_predecesor.concat(nuevo);
    i++;
  }
  parar=PARAR;
  //  SATURACION MOVIL     /////////////
  sat_d=refVel.toFloat();                            //HABILITAR PARA ALGORITMO DE SATURACION PID PREDECESOR
  //if(refVel.toFloat()>=0){
  //  sat_d=1*refVel.toFloat() + 1;
  //}
  //else{
  //  sat_d=1*(-refVel.toFloat()) + 1;
  //}
  //Serial.println(PARAR);
  //Serial.println(VEL);
  //Serial.println(refVel);
  /////////////////////////////////////
  //vel_crucero=VEL.toFloat();                                 //HABILITAR PARA ALGORITMO DE SWITCHEO CURVATURA 
  curvatura_predecesor=CURVA_predecesor.toFloat();
}
/*
void udp_transm() {
  t_actual = millis() - t_com_predecesor;
  if (curva > 10 && t_actual >= 300) {
    udp.beginPacket(IP_sucesor, puerto_sucesor);
    udp.printf("curva");
    udp.endPacket();
    t_com_predecesor = millis();
  }
}*/
void udp_transm() {
  t_actual = millis() - t_com_predecesor;
  if (t_actual >= 100) {
    cadena = "V/" + parar + "/" + String(Input_vel) + "/" + String(vel_ref) + "/" + String(curvatura);
    cadena.toCharArray(msg, cadena.length() + 1);
    udp.beginPacket(IP_sucesor, puerto_sucesor);
    udp.printf(msg);
    udp.endPacket();
    t_com_predecesor = millis();
  }
}

void udp_check() {
 
  cadena = String(EtiquetaRobot) + "," + String(IP_sucesor) + ": Encendido";
//Serial.println(cadena);
  cadena.toCharArray(msg, cadena.length() + 1);
  udp.beginPacket(IP_monitoreo, puerto_monitoreo);
  udp.printf(msg);      //
  udp.endPacket();

}


void udp_monitor() {
  //t_actual = millis() - t_monitoreo;
  //if(t_actual>=20){
  cadena = String(EtiquetaRobot) +"," + String(t_actual) +"," + String(Input_d) + "," + String(d_ref) + "," + String(vel_ref) + "," + String(Input_vel) + "," + String(Input_theta) + "," + String(Output_d) + "," + String(Output_vel) + "," + String(Output_theta)+ "," + String(curvatura)+ "," + String(vel_crucero)+ "," + String(curvatura_predecesor)+ "," + String(control);
  //cadena = String(EtiquetaRobot) +"," + String(t_actual) +"," + String(Input_d) + "," + String(d_ref) + "," + String(vel_ref) + "," + String(Input_vel) + "," + String(recta) + "," + String(a_curvatura) + "," + String(b_curvatura) + "," + String(c_curvatura)+ "," + String(curvatura)+ "," + String(vel_crucero)+ "," + String(curvatura_predecesor)+ "," + String(control);
  cadena.toCharArray(msg, cadena.length() + 1);
  udp.beginPacket(IP_monitoreo, puerto_monitoreo);
  udp.printf(msg);      //
  udp.endPacket();
  //  t_monitoreo = millis();
  //}
  //udp.flush();
}
///////////////////////////////CONFIGURACION WIFI////////////////
void setup_wifi() {
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  //while (WiFi.status() != WL_CONNECTED) {
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    WiFi.begin(ssid, password);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  udp.begin(puerto_local);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), puerto_local);

  //  udp.listen(1234);
}

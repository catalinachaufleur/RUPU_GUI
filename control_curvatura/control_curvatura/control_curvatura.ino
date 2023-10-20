#include <esp_wifi.h>
#include <WiFi.h>
#include <analogWrite.h> //ESP32 LEDC
#include <Encoder.h>
#include <Wire.h> //I2C
#include <VL53L0X.h>


///     WIFI
///////////////////////////////////////
//     Configuración RED   ///////////
///////////////////////////////////////
#define ssid "fvp"    
#define password "nomeacuerdo"

#define IP_monitoreo "192.168.1.100"     //ip del dispositivo que va a supervisar los datos 
#define puerto_monitoreo 1234           //puerto de envio UDP monitoreo
#define IP_sucesor "192.168.1.105"   //ip del robot sucesor
#define puerto_sucesor 1111          //puerto del robot sucesor
#define puerto_local 1111               //puerto local
////////
#define EtiquetaRobot "L"   // "L": Robot0 (lider)   "S": robot2    "T": Robot3    "O": Robot4 
#define led 2
#define radio_rueda 2.15 //RADIO EN [CM]
#define l 5.6 // l corresponde a la distancia entre las ruedas en cm
#define N 0.01 // Modulo de REDUCCION 
#define CPR 28 // Cuentas por revolucion encoders
#define d1 52
#define d2 32
//
/*  Pines motor 1 (derecho)*/
#define ain1  16
#define ain2  27
#define pwm_a  17

/*  Pines motor 2 (izquierdo)*/
#define bin1  13
#define bin2  12
#define pwm_b  14

#define resolucionPWM 1023
/////////////////////////////SUPERFICIE
#define linea 1  // valor logico 1 corresponde a una pista con trayectoria color blanco; Valor lógico 0 corresponde a una pista con trayectoria color negro. 



// MAQUINA DE ESTADOS
#define inicio 0
#define calibracion 1
#define controlLoop 2
byte estado=0;
byte estado_siguiente=0;
byte calibrar=0;
String parar = "si"; //permite saber si el robot se salió de la pista


/////////////////////////////////////////////////////////////// VARIABLES CONTROLADORES PID
//Define Variables we'll be connecting to PID de posicion
double Input_theta, Output_theta;
double theta_ref = 0;
//Define the aggressive and conservative Tuning Parameters
/*PID posición*/
double Kp_theta = 2000;//64.078;//147.657974619537;//60;
double Ki_theta = 4500;//145.3619;//555.734047342947;//150;
double Kd_theta = 60;//7.0616;//8.30454187876464;//1;

//Define Variables we'll be connecting to PID de Velocidad
double Input_vel, Output_vel;
double Output_vel_ant = 0;
double vel_ref = 0;
double sp_vel = 0;
double vel_crucero = 15;

//Define the aggressive and conservative Tuning Parameters
/*PID velocidad*/
double Kp_vel = 20.3;//100;//49.9757241214599;//130;
double Ki_vel = 145.3;//282.271150682254;//130;
double Kd_vel = 0;//0.197722771627088;//0;

//Define Variables we'll be connecting to PID de distancia
double Input_d, Output_d;
double d_ref = 10;
double error_d;
float delta = 0.1;

//Define the aggressive and conservative Tuning Parameters
/*PID velocidad*/
double Kp_d = 4;//1.5;//8.0013;
double Ki_d = 3;//11;//5.6025;
double Kd_d = 0;//0.1;//1.0077;
//Specify the links and initial tuning parameters
String PID_theta="MANUAL";
double sat_theta=1023;
double error_ant_theta=0;
double integral_theta=0;
String PID_vel="MANUAL";
double sat_vel=800;
double error_ant_vel=0;
double integral_vel=0;
String PID_d="MANUAL";
double sat_d=30;
double error_ant_d=0;
double integral_d=0;
/////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////// VARIABLES UDP
WiFiUDP udp;
String cadena;
char msg[128];
char paquete_entrante[64];  // buffer for incoming packets
unsigned long t_com_predecesor, t_monitoreo;
////////////////////////////////////////////////////////////

unsigned long t_actual;     //TIMER GENERAL
unsigned long t_controlador;

//////////SENSORES
double ang_vel;
double v_r[] = {0, 0, 0, 0, 0};
double v_l[] = {0, 0, 0, 0, 0};
double a_sl=0;
double a_sr=0;
double b_sl=0;
double b_sr=0;
double c_sl=0;
double c_sr=0;
double a_s=0;
double b_s=0;
double c_s=0;
unsigned long t_arco;
byte recta=0;
double a_curvatura=0;
double b_curvatura=0;
double c_curvatura=0;
double curvatura=0;
double curvatura_predecesor=0;
unsigned long t_svel;
double cuenta=0;

VL53L0X sensor;     //SENSOR DE DISTANCIA I2C

Encoder encoder_der(5, 23);
Encoder encoder_izq(18, 19);

byte control=1;

void setup()
{
  Serial.begin(115200);
  Serial.println("setup!");
  WiFi.mode(WIFI_STA);
  esp_wifi_set_ps(WIFI_PS_NONE);
  setup_wifi(); // ver abajo
  configuracion_sensor_d();
  //
  pinMode(led, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);

}

void loop(){
  //Serial.print("ESTADO   :");
  //Serial.println(estado);
  switch (estado) {
    case inicio:
      //udp_check();
      ciclo_de_inicio();
      break;
    case calibracion:
      calibrarSensores();
      calibrar=0;
      break;
    case controlLoop:
      ciclo_de_control();
      break;  
    default:
      ciclo_de_inicio();
      break;
  }
  /////////////// transiciones
  if(estado==inicio && calibrar){
    estado_siguiente=calibracion;
  }
  else if(estado==inicio && parar=="si"){
    estado_siguiente=inicio;
  }
  else if(estado==inicio && parar=="no"){
    estado_siguiente=controlLoop;
  }
  else if(estado==calibracion){
    estado_siguiente=inicio;
  }
  else if(estado==controlLoop && parar=="no"){
    estado_siguiente=controlLoop;
  }
  else if(estado==controlLoop && parar=="si"){
    estado_siguiente=inicio;
  }
  else{
    estado_siguiente=inicio;
  }
  estado=estado_siguiente;
}

void ciclo_de_inicio(){
  udp_recep();
  PID_theta="MANUAL";
  PID_vel="MANUAL";
  PID_d="MANUAL";
  error_ant_d=0;
  integral_d=0;
  error_ant_vel=0;
  integral_vel=0;
  error_ant_theta=0;
  integral_theta=0;
  Output_d=0;
  Output_vel=0;
  Output_theta=0;
  d_ref = distancia();
  sp_vel = 0;
  Input_vel=0;
  vel_ref=0;
  motor(0,0);
  encoder_der.write(0);
  encoder_izq.write(0);
  udp_transm();
}


void ciclo_de_control(){
  udp_recep();
  Input_d = distancia();
  if(EtiquetaRobot!="L"){
    error_d = Input_d - d_ref;
  }
  else{
    error_d=0;
  }
  velocidades();
  curvatura_pista();
  //control=((curvatura_predecesor <= 0.01) && (curvatura <= 0.01));      // HABILITA ALGORITMO DE SWITCHEO CURVATURA
  control=1;                                                              // DESAVILITA ALGORITMO CURVATURA
  if(Output_vel<0){
    Input_theta=-getposition(0)/d2;
  }
  else{
    Input_theta=getposition(1)/d1;
  }
  if ((abs(error_d) >= delta + 1) || EtiquetaRobot=="L") {
    PID_theta="AUTO";
    PID_vel="AUTO";
    if(control){
      PID_d="AUTO";
    }
    else{
      PID_d="MANUAL";
      Output_d=vel_crucero;
      error_ant_d=0;
      integral_d=vel_crucero/Ki_d - error_d*0.04;
    }
    if(EtiquetaRobot=="L"){
      PID_d="MANUAL"; 
      Output_d = 0;
      error_ant_d=0;
      integral_d=0;
      error_d =0;
    }
  }
  if (abs(Input_vel) <= 6 && abs(Input_theta) <= 0.015 && ((abs(error_d) < delta) && (sp_vel==0 || EtiquetaRobot!="L"))) {
    PID_d="MANUAL";
    PID_vel="MANUAL";
    PID_theta="MANUAL";
    Output_d = 0;
    Output_vel = 0;
    Output_theta = 0;
    error_ant_d=0;
    integral_d=0;
    error_ant_vel=0;
    integral_vel=0;
    error_ant_theta=0;
    integral_theta=0;
  }
  udp_transm();                                                   //HABILITA LA TRANSMSION DE DATOS ENTRE ROBOTS
  t_actual=millis()-t_controlador;
  if(t_actual>=40){
    //Output_d=calculoPID(Input_d, d_ref,error_ant_d, integral_d, Kp_d, Ki_d, Kd_d, sat_d, PID_d, Output_d, "INVERSO");     //HABILITAR PARA CONTROLADOR PID SIN COMUNICACION Y SWITCHEO CURVATURA
    Output_d=calculoPIDd(Input_d, d_ref,error_ant_d, integral_d, Kp_d, Ki_d, Kd_d, sat_d, PID_d, Output_d, "INVERSO"); //HABILITA CALCULO DE PID CON SATURACION PREDECESOR
    vel_ref= Output_d *(EtiquetaRobot!="L") + (EtiquetaRobot=="L")*sp_vel;
    Output_vel=calculoPID(Input_vel, vel_ref, error_ant_vel, integral_vel, Kp_vel, Ki_vel, Kd_vel, sat_vel, PID_vel, Output_vel, "DIRECTO");
    Output_theta=calculoPID(Input_theta, theta_ref, error_ant_theta, integral_theta, Kp_theta, Ki_theta, Kd_theta, sat_theta, PID_theta, Output_theta, "DIRECTO");
    udp_monitor();
    t_controlador=millis();
  }
  motor(Output_vel - Output_theta, Output_vel + Output_theta);
}

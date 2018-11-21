#include <VirtualWire.h>
#include <VirtualWire_Config.h>
/*------------------- variable initializations for ultrasonic sensor ------------------------*/
int Trigger = 7;
int Echo = 12;
//int Buzzer_pin = 11;
int Time_taken;
unsigned int Distance;
int a;
int height;
int per;
/*-------------------  variable initializations for soilmoisture sensor   ------------------------*/
int smsensor_pin = A2;
int smsensor_pin1 = A1;
char state[10]={0} ;
char state1[10]={0} ;
char state2[10]={0} ;
int smv ;
int smv1;
int motorpin = 13;
int motorpin1 = 4;

/*-------------------  variable initializations for raindrop sensor (rdp)  sensor   ------------------------*/

const int sensorMin = 0;     // sensor minimum
const int sensorMax = 1024;  // sensor maximum
int rdpsensor_pin=A3;
int flag;

/* -----------------   code begins ------------------------------*/
void setup() {
   pinMode(Trigger,OUTPUT);
   pinMode(Echo,INPUT);
  pinMode(motorpin,OUTPUT);
  pinMode(motorpin1,OUTPUT);
  
   Serial.begin(9600);
}
void loop() {
  
    height=10;
    smv=0;
    smv1=0;
    
     /*----------- read ultrasonic sensor value--------------------*/
    digitalWrite(Trigger, LOW);
    delayMicroseconds(2);
  int f=0;
    digitalWrite(Trigger, HIGH);
    delayMicroseconds(10);
  
    digitalWrite(Trigger, LOW);// when this trigger pin will low automatically echo pin will get high.
                             // And with the help of pulse in function we are getting that time for which echo pin is enabled
                             
  
    Time_taken = pulseIn(Echo,HIGH);
  
    Distance = (Time_taken/2)/29.1;//here time is converting into distance . from meter to cm

     /*----------- distance stored in Distance is mapped to a vaariable a in the below fassion which is later used to determine the amount of water released to water the plant on the basisi of water level in the tank --------------------*/
    if(Distance<=3){
        a=60;
    }
    else{
      a=(Distance*60)/3;
    }
  
   
   
 /*----------- states 0 indicates actuators are off   --------------------*/
   state[0]='n';
   state[1]='o';
   state[2]=0;
   
   state1[0]='n';
   state1[1]='o';
   state1[2]=0;
   
   
 /*--------- read values of soil moisture and rain drop  sensors  -----*/  
    smv= analogRead(sensor_pin);
    smv = map(smv,1023,0,0,100);
     smv1= analogRead(sensor_pin1);
    smv1 = map(smv1,1023,0,0,100);
   int rdpsensorReading = analogRead(rdpsensor_pin); 
  
  
    /* -----------------   flag is a variable maintained to note the rain conditions  , that is if flag is 0, no rainfall, flag is 1 then it's raining ------------------------------*/
   if(rdpsensorReading<100)
     flag=0;
   else
     flag=1;
 
 
 if(flag == 0 )                                       // if it is not raining
 {
   
   if(smv<=20 && smv1>20)                            // if soil moisture of plant 1 is less than threshold (20) and  soil moisture of plant 2 is greater than threshold (20)
   {
    
     state[0]='y';                                    // set  the states
     state[1]='e';
     state[2]='s';
     state[3]=0;
     state1[0]='n';
     state1[1]='o';
     state1[2]=0;
     
    
     
     digitalWrite(motorpin,HIGH);                                  // actuator 1 - on 
     digitalWrite(motorpin1,LOW);                                   // actuator 2 - off 
      
      
     while(map(analogRead(smsensor_pin),1023,0,0,100)<=a)                 // water plant 1 till its soil moisture becomes greater than value 'a'
     {
       rdpsensorReading = analogRead(rdpsensor_pin);
       if( rdpsensorReading<100)                                         // chek if it is raining every time 
       {
         if(map(analogRead(smsensor_pin1),1023,0,0,100)<=20)             // chek if meanwhile plant 2's soil moisture  has become  lesser than the threshold
         {
         break;
         }
                                                                                  
        
      digitalWrite(motorpin,HIGH);                                                       // contimue to water  
      
      digitalWrite(Trigger, LOW);                                                       // every iteration read the values of all  sensors
    delayMicroseconds(2);
  int f=0;
    digitalWrite(Trigger, HIGH);
    delayMicroseconds(10);
  
    digitalWrite(Trigger, LOW);
  
    Time_taken = pulseIn(Echo,HIGH);
  
    Distance = (Time_taken/2)/29.1;
    
                                                                                              // print the readings in order to be read by raspberry pi through serial communucation
     
      Serial.print(Distance);
      Serial.print("  ");
      Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state);
      Serial.print("  ");
         Serial.print(smv1); 
      Serial.print("  ");
      Serial.print(state1);
      Serial.print("  ");
      Serial.println(rdpsensorReading);
       }
       else
       {
         // when watering ends reset the state 
         digitalWrite(motorpin,LOW);
         state[0]='n';
         state[1]='o';
         state[2]=0;
         Serial.print(Distance);
        Serial.print("  ");
        Serial.print(smv); 
        Serial.print("  ");
        Serial.print(state);
        Serial.print("  ");
        Serial.print(smv1); 
        Serial.print("  ");
        Serial.print(state1);
        Serial.print("  ");
        Serial.println(rdpsensorReading);
        delay(500);
        break;
       }
     delay(500);
     }
      // reset states and pins
     digitalWrite(motorpin,LOW);
     state[0]='n';
     state[1]='o';
     state[2]=0;
     
     Serial.print(Distance);
    Serial.print("  ");
    Serial.print(smv); 
    Serial.print("  ");
    Serial.print(state);
    Serial.print("  ");
     Serial.print(smv1); 
     Serial.print("  ");
     Serial.print(state1);
    Serial.print("  ");
     Serial.println(rdpsensorReading);
      delay(500);
    }
    
   else if(smv1<=20 && smv>20)                               // if soil moisture of plant 2 is less than threshold (20) and  soil moisture of plant 1 is greater than threshold (20)
   {
     state1[0]='y';                                          // set  the states
     state1[1]='e';
     state1[2]='s';
     state1[3]=0;
     
        state[0]='N';
     state[1]='O';
     state[2]=0;
     
     
     digitalWrite(motorpin1,HIGH);                                             // actuator 2 - on 
    
       digitalWrite(motorpin,LOW);                                            // actuator 1 - off 
     
   
     while(map(analogRead(smsensor_pin1),1023,0,0,100)<=a)                  // water plant 2 till its soil moisture becomes greater than value 'a' 
     {
       rdpsensorReading = analogRead(rdpsensor_pin);
       if( sensorReading<100)                                                 // chek if it is raining every time 
       {
         
          if(map(analogRead(smsensor_pin),1023,0,0,100)<=20)                     // chek if meanwhile plant 1's soil moisture  has become  lesser than the threshold
         {
         break;
         }
         
         
          digitalWrite(motorpin1,HIGH);                                           // continue to  water
          
          
          
          digitalWrite(Trigger, LOW);                                           // take readings of all sensors in every iteration
          delayMicroseconds(2);
           int f=0;
          digitalWrite(Trigger, HIGH);
          delayMicroseconds(10);
          digitalWrite(Trigger, LOW);
          Time_taken = pulseIn(Echo,HIGH);
          Distance = (Time_taken/2)/29.1;
    
                                                                                         // print the readings in order to be read by raspberry pi through serial communucation
      Serial.print(Distance);
      Serial.print("  ");
       Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state);
      Serial.print("  ");
      Serial.print(smv1); 
      Serial.print("  ");
      Serial.print(state1);
      Serial.print("  ");
      Serial.println(rdpsensorReading);
       }
       else
       {
          // when watering ends reset the state and pin
         digitalWrite(motorpin1,LOW);
         state1[0]='n';
     state1[1]='o';
     state1[2]=0;
         Serial.print(Distance);
    Serial.print("  ");
     Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state);
      Serial.print("  ");
    Serial.print(smv1); 
    Serial.print("  ");
    Serial.print(state1);
    Serial.print("  ");
      Serial.println(rdpsensorReading);
      delay(500);
      break;
       }
      delay(500);
     }
     
     // reset states and pins
     digitalWrite(motorpin1,LOW);
     state1[0]='n';
     state1[1]='o';
     state1[2]=0;
   
    Serial.print(Distance);
    Serial.print("  ");
     Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state);
      Serial.print("  ");
    Serial.print(smv1); 
    Serial.print("  ");
    Serial.print(state1);
    Serial.print("  ");
      Serial.println(rdpsensorReading);
      delay(500);
    }
    
   
    
 else if(smv<=20 && smv1<=20)                                                                      // if soil moisture of planta 1 and  2 are less than threshold (20) 
   {
     state[0]='y';                                                                           // set  the states
     state[1]='e';
     state[2]='s';
     state[3]=0;
     
     state1[0]='y';
     state1[1]='e';
     state1[2]='s';
     state1[3]=0;
     
     digitalWrite(motorpin,HIGH);                                                            // actuator 1 - on
     digitalWrite(motorpin1,HIGH);                                                            // actuator 2 - on
    
    
    
    
     while(map(analogRead(smsensor_pin),1023,0,0,100)<=a && map(analogRead(smsensor_pin1),1023,0,0,100)<=a )                        // water plant 1 and 2 till one of their soil moisture becomes greater than value 'a' 
     {
       rdpsensorReading = analogRead(rdpsensor_pin);
       if( rdpsensorReading<100)                                                                                                         // chek if it is raining every time 
       {
         
         
      digitalWrite(motorpin,HIGH);                                                                                                          // continue to  water
      digitalWrite(motorpin1,HIGH);
      
      
      digitalWrite(Trigger, LOW);
    delayMicroseconds(2);
  int f=0;
    digitalWrite(Trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(Trigger, LOW);  
    Time_taken = pulseIn(Echo,HIGH);
  
    Distance = (Time_taken/2)/29.1;
    
     
      Serial.print(Distance);                                                                                       // take readings of all sensors in every iteration
      Serial.print("  ");      
      Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state);
      Serial.print("  ");
      Serial.print(smv1); 
      Serial.print("  ");
      Serial.print(state1);
      Serial.print("  ");
      Serial.println(rdpsensorReading);
       }
       else
       {
       //when watering ends reset the state and pin
         digitalWrite(motorpin,LOW);
         digitalWrite(motorpin1,LOW);
         state[0]='n';
     state[1]='o';
     state[2]=0;
     
         state1[0]='n';
     state1[1]='0';
     state1[2]=0;
     
         Serial.print(Distance);
    Serial.print("  ");
    Serial.print(smv); 
    Serial.print("  ");
    Serial.print(state);
    Serial.print("  ");
    Serial.print(smv1); 
    Serial.print("  ");
    Serial.print(state1);
    Serial.print("  ");
      Serial.println(rdpsensorReading);
      delay(500);
      break;
      
       }
      delay(500);
     }
      // restet states and pins 
     digitalWrite(motorpin,LOW);
     digitalWrite(motorpin1,LOW);
     state[0]='n';
     state[1]='o';
     state[2]=0;
     
     state1[0]='n';
     state1[1]='0';
     state1[2]=0;
    
    Serial.print(Distance);
    Serial.print("  ");
    Serial.print(smv); 
    Serial.print("  ");
    Serial.print(state);
    Serial.print("  ");
    Serial.print(smv1); 
    Serial.print("  ");
    Serial.print(state1);
    Serial.print("  ");
      Serial.println(rdpsensorReading);
      delay(500);
    }
   
      Serial.print(Distance);
      Serial.print("  ");
      Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state); 
      Serial.print("  ");
      Serial.print(smv1); 
      Serial.print("  ");
      Serial.print(state1); 
      Serial.print("  ");
      Serial.println(rdpsensorReading);
      


  delay(500);

   }
   Serial.print(Distance);
      Serial.print("  ");
      Serial.print(smv); 
      Serial.print("  ");
      Serial.print(state); 
      Serial.print("  ");
      Serial.print(smv1); 
      Serial.print("  ");
      Serial.print(state1); 
      Serial.print("  ");
      Serial.println(rdpsensorReading);
        delay(500);
}

#ifndef MAIN_H
#define MAIN_H

#include <avr/pgmspace.h> // libs for working with flash, writing and reading text constants 
#include "Apps/apps.h"  // local app library 
#include "SimpleCLI.h" // https://github.com/spacehuhn/SimpleCLI
#include "Fsm.h"  //https://github.com/jonblack/arduino-fsm
#include "Apps/fsm_app.h"

// debug macros for an easy access to Serial.print function
// 
//#define DEBUG  // enable debug macros uncomment this line 
// use case : insert DEBUG_PRINT(x) in code. 
//

#ifdef DEBUG
 #define DEBUG_PRINT(x)        Serial.print (x)
 #define DEBUG_PRINTDEC(x)     Serial.print (x, DEC)
 #define DEBUG_PRINTLN(x)      Serial.println (x)
#else
 #define DEBUG_PRINT(x)
 #define DEBUG_PRINTDEC(x)
 #define DEBUG_PRINTLN(x)
#endif

//***********************************************************
//******** CONSTANTS ****************************************
//***********************************************************

#define SoftwareVersion 0.1 //current build 
#define UARTSpeed 115200    //UARTboudrate setup 
#define strlenth 55         // default leng of text array
#define defRes 10000       // default value of resistor 


//***********************************************************
//******** VARIABLES ****************************************
//***********************************************************



const int slaveSelectPin = 10; //   Pin 10 is used as SPI Slave Select (SS)


typedef struct{
  int CyrrentRes[8];
  int SetRes[8];
} ResValue;




/*
 *  Divider ratio constants 
 */

#define Kdiv 3.97








#endif  // MAIN_H
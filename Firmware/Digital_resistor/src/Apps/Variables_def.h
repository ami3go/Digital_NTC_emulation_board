#ifndef VARIABLES_DEF_H
#define VARIABLES_DEF_H


#if defined(ARDUINO) && ARDUINO >= 100
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif


#define SoftwareVersion 3.0 //current build 
#define UARTSpeed 115200    //

#define strlenth 55 

#define defRes 10000    //

typedef struct{
  int CyrrentRes[8];
  int SetRes[8];
} ResValue;


/*
 *  Divider ratio constants 
 */

#define Kdiv 3.97






#endif  

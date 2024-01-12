#ifndef MAIN_H
#define MAIN_H

#include <avr/pgmspace.h> // libs for working with flash, writing and reading text constants 
#include "Apps/apps.h"
#include "SimpleCLI.h" // https://github.com/spacehuhn/SimpleCLI
#include "Fsm.h"  //https://github.com/jonblack/arduino-fsm

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








#endif  // MAIN_H
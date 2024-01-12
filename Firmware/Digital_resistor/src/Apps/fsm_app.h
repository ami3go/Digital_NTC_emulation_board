#ifndef FSM_APP_H
#define FSM_APP_H
#include "Fsm.h"
#include <Arduino.h>

/*********State Machine Trasition Signals *******************/

#define GoTo_Main  0 
#define GoTo_Trig 1 
#define GoTo_Set 2


/************************************************************
 ******** Starte machine applications ***********************
 ************************************************************/

 // Main State 
void enter_start();
void on_start();
void exit_start();


 // Main State 
void enter_main();
void on_main();
void exit_main();

// Trigget
void enter_trig();
void on_trig();
void exit_trig(); 

// Setting
void enter_set();
void on_set();
void exit_set();



#endif
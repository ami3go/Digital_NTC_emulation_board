#include "fsm_app.h"


/************************************************************
 ******** Starte machine applications ***********************
 ************************************************************/


 // Initialization 
void enter_start(){
     Serial.println("Enter Start");
};
void on_start(){
    Serial.println("On Start");
};
void exit_start(){
    Serial.println("Exit Start");
};



 // Main State 
void enter_main(){
    Serial.println("Enter MAin");
};
void on_main(){
       Serial.println("On MAin");
};
void exit_main(){
       Serial.println("Exit MAin");
};

// Trigget
void enter_trig(){
       Serial.println("Enter Trig");
};
void on_trig(){
      Serial.println("On Trig");
};
void exit_trig(){
      Serial.println("EXit Trig");
}; 

// Setting
void enter_set(){
      Serial.println("Enter Set ");
};
void on_set(){
      Serial.println("On Set ");
};
void exit_set(){
      Serial.println("Exit Set ");
};

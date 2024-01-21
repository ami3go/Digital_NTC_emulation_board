#include <Arduino.h>
#include "main.h"
#include <SPI.h>





// put string constant into FLASH memory to reduse RAM usage

const static char StrStart_flash[strlenth]   PROGMEM = "START:  <Click>    N Runs:";



// Create CLI Object
SimpleCLI cli;   

// // Commands
// Command cmdTrig;
// Command cmdSetRes;
// Command cmdGetRes;
// // Command cmdSetOfftime;
// // Command cmdSetNrep;
// // Command cmdGetstatus;
// // Command cmdGetVload;
Command cmdHelp;

void errorCallback(cmd_error* e); 

//***********************************************************
//******** VARIABLES ****************************************
//***********************************************************




 


/*********State Machine Applications ************************/
 
/*********Finite Start Machine. State list: ************************/
State state_start(&enter_start, &on_start,&exit_start); //initial state
State state_main(&enter_main, &on_main, &exit_main); //fill up default configuration
State state_trig(&enter_trig, &on_trig, &exit_trig);  
State state_set(&enter_set, &on_set, &exit_set);


// Fsm fsm(&state_int); // Starting state  





/****************Arduino setUp app start *********************************************
 ************************************************************************************* 
 *************************************************************************************/

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(UARTSpeed);
  
  // Initialize SPI communication
  pinMode(slaveSelectPin, OUTPUT); 
  SPI.begin();

/******* Command Line interface int ********************************/
//Command start; getstatus; getvload; getvload ; 
//Command set, setontime; setofftime, set nrep ;
//Command help;

 cmdHelp = cli.addCmd("help"); //Help command settigns 
      const static char StrHelp[] PROGMEM = "Display help massage, command list and arguments ";
      cmdHelp.setDescription(StrHelp);

cli.setOnError(errorCallback); // Set error Callback


/***********FSM TRANSITIONS  Settings start **************************************************************************/
// /*1*/  fsm.add_timed_transition(&state_int,          &state_default_conf,  HomeScreenShowTime,         NULL);  // timed tansition 
// /*2*/  fsm.add_timed_transition(&state_default_conf, &state_waiting_start, DefCongToWaitingStartDelay, NULL);  // timed tansition  

// /*3*/  fsm.add_transition(&state_waiting_start, &state_setup_ontime,   GoTo_OnTimeSetUp, NULL); // hold encoder button to  change settings 




}



/*************** Arduino MAIN LOOP *****************************************************/
void loop() {
  // fsm.run_machine();// just keep state machine alive
  delay(1);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(500);                      // wait for a second
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(500);

  /*********** Command Line interface section *********************************/

/****    Check if something available on uart ***********************************/
   if (Serial.available()) {
        String input = Serial.readStringUntil('\n');// Read out string from the serial monitor
        Serial.print(F("# "));// Echo the user input
        Serial.println(input);  
        cli.parse(input); // Parse the user input into the CLI
    }; /*  */

   if (cli.available()) {
      // Read out string from the serial monitor
      Command cmd = cli.getCommand();
  //     if(cmd == cmdSet) {
  //       Argument ontimeArg  = cmd.getArgument(F("ontime"));
  //       Argument offtimeArg = cmd.getArgument(F("offtime"));
  //       Argument nrepArg    = cmd.getArgument(F("nrep"));

  //       int  ontime_var  = ontimeArg.getValue().toInt()/10;
  //       int  offtime_var = offtimeArg.getValue().toInt()/10;
  //       int  nrep_var    = nrepArg.getValue().toInt();
    
  //       CHAvar.ONtime  = setValueInRange(CHAvar.ONtime, ontime_var,ONtimeMIN,ONtimeMAX);
  //       CHAvar.OFFtime = setValueInRange(CHAvar.OFFtime, offtime_var,OFFtimeMIN,OFFtimeMAX);
  //       CHAvar.Ncycles = setValueInRange(CHAvar.Ncycles, nrep_var,NcyclesMIN,NcyclesMAX);  

  
        
  // }
     //Run generator CMD!
    //  if(cmd == cmdStart) {
    //   Argument delayArg = cmd.getArgument(F("delay"));
    //   int  delayval = delayArg.getValue().toInt();
    //   delayval = setValueInRange(0, delayval ,0, 5000);
    //   if (delayval!= 0) delay(delayval);
    //   fsm.trigger(GoTo_Running);  
    //  };
     //Return variable paramentes 
    //  if(cmd == cmdGetstatus) printStatusToSerial( &CHAvar, Nstarts, Vout.AvarageValue);

    //  if(cmd == cmdGetVload) printVloadToSerial(Vout.AvarageValue);
          
     // Return Help massage.   
     if(cmd == cmdHelp) printHelptoSerial();
     
    //  if(cmd == cmdSetOntime) {
    //   Argument ontimeArg = cmd.getArgument(F("ontimevalue"));
    //   int  ontimeval = ontimeArg.getValue().toInt()/10;
    //   CHAvar.ONtime = setValueInRange(CHAvar.ONtime, ontimeval ,ONtimeMIN, ONtimeMAX);
    //   UpdateValuesDisplOne(); 
    //     }
    //  if(cmd == cmdSetOfftime) {
    //   Argument offtimeArg = cmd.getArgument(F("offtimevalue"));
    //   int  offtimeval = offtimeArg.getValue().toInt()/10;
    //   CHAvar.OFFtime = setValueInRange(CHAvar.OFFtime, offtimeval ,OFFtimeMIN, OFFtimeMAX);
    //   UpdateValuesDisplOne(); 
    //  }
    //   if(cmd == cmdSetNrep) {
    //   Argument nrepArg = cmd.getArgument(F("nrepvalue"));
    //   int  nrepval = nrepArg.getValue().toInt();
    //   CHAvar.Ncycles = setValueInRange(CHAvar.Ncycles, nrepval,NcyclesMIN,NcyclesMAX); 
    //   UpdateValuesDisplOne(); 
    //  } 


     
    }; /*End of  if (cli.available()) */
/*
 * CLI END section
 */




};/*************** END OF Arduino MAIN LOOP ******************************************/



/***********************************************************
 * *********************************************************
 * Command line interface section 
 * *********************************************************
 * *********************************************************
 */
 // Callback in case of an error

void errorCallback(cmd_error* e) {
    CommandError cmdError(e); // Create wrapper object

    Serial.print(F("ERROR: "));
    Serial.println(cmdError.toString());

    if (cmdError.hasCommand()) {
        Serial.print(F("Did you mean \""));
        Serial.print(cmdError.getCommand().toString());
        Serial.println(F("\"?"));
    }
};
#include <Arduino.h>
#include "main.h"
#include <SPI.h>


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





/****************Arduino setUp app start *********************************************
 ************************************************************************************* 
 *************************************************************************************/

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(UARTSpeed);


/******* Command Line interface int ********************************/
//Command start; getstatus; getvload; getvload ; 
//Command set, setontime; setofftime, set nrep ;
//Command help;

 cmdHelp = cli.addCmd("help"); //Help command settigns 
      const static char StrHelp[] PROGMEM = "Display help massage, command list and arguments ";
      cmdHelp.setDescription(StrHelp);

cli.setOnError(errorCallback); // Set error Callback

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
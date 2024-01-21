#include "apps.h"


// help messange will add later 
void printHelptoSerial (void){
  Serial.println(F("|----------------Supported command list:-------------------------------|"));
  Serial.println(F("| 1 | start | Start generating, trigger run button via uart            |"));
  Serial.println(F("| * | type: start  - 'start immideatly'                                |"));
  Serial.println(F("| * | type: start <delay_value=0-5000ms>; example: start 100           |"));
  Serial.println(F("| E:| example: start 100                                               |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 2 | set   | Setup pulse generator parameters ON time, Off time, Nrep |"));
  Serial.println(F("| * | type: set -ontime <val us> -offtime <val us> -nrep <val>         |"));
  Serial.println(F("| * | On/Off time value in range 100 us - 6500 us, Nrep in range 1-500 |"));
  Serial.println(F("| E:| example: set -ontime 250 -offtime 300 -nrep 5                    |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 3 | set ON time | Set the ON pulse duration time, in us              |"));
  Serial.println(F("| * | type: setontime <val us>; example: setontime 250 [100-6500 us]   |"));
  Serial.println(F("| E:| example: setontime 250 [On time value in range 100 us - 6500 us] |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 4 | set OFF time | Set the OFF pulse duration time, in us            |"));
  Serial.println(F("| * | type: setofftime <val us>; example: setofftime 500 [100-6500 us] |"));
  Serial.println(F("| E:| example: setofftime 500[OFF time value in range 100 us - 6500 us]|"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 5 | set Nrep | Set nubmer of pulses to be geenerated on a signle run |"));
  Serial.println(F("| * | type: setnrep <val times>; example: setnrep 20  [1-500]          |"));
  Serial.println(F("| E:| example: setnrep 20 [Nrep value in range 1 - 500  ]              |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 6 | status|Returns current generator setting and load voltage        |"));
  Serial.println(F("| E:| type: getstatus                                                  |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 7 | Vload |Returns measured voltage on load connector                |"));
  Serial.println(F("| E:| type: getvload                                                   |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
  Serial.println(F("| 8 | help  | Display this massage                                     |"));
  Serial.println(F("| E:| type: help                                                       |"));
  Serial.println(F("|----------------------------------------------------------------------|"));
};
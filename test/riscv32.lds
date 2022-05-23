ENTRY(_start)

/* memory starts at 0x80000000 and ends at 0x88000000 */
STACK_SIZE = 0x2000;

SECTIONS {
  . = 0x80000000;
  .init : {*.(init)}
  .text : {*.(text)}
  .data : {*.(data)}
  .stack : {*.(stack)}
   __stackTop = .;
   . = . + STACK_SIZE;
  /*TODO: make .dataOut which starts here and
  write output to named variables, just like input*/
  __dataOutTop = .;
}

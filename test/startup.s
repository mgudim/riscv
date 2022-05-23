.section .init, "ax"
.globl _start

_start:
  # set up the stack pointer
  la sp, __stackTop
  j main

.section .init, "ax"
.globl _end

_end:
  # halt here
  j _end

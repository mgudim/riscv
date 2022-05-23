.section .text, "ax"
.globl main
main:
  # read the contents of "greeting" variable into registers a1, a2, a3
  lui  a0, %hi(greeting)
  lw a1, %lo(greeting)(a0)
  lw a2, %lo(greeting + 4)(a0)
  lw a3, %lo(greeting + 8)(a0)
  lui  a0, %hi(intVar)
  lw a4, %lo(intVar)(a0)

  # The variable __dataOutTop is defined in the linker script. This is where the output should go.
  lui  a0, %hi(__dataOutTop)
  sw a1, %lo(__dataOutTop)(a0)
  sw a2, %lo(__dataOutTop + 4)(a0)
  sw a3, %lo(__dataOutTop + 8)(a0)
  sw a4, %lo(__dataOutTop + 12)(a0)
  j _end

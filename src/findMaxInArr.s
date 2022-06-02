.section .text, "ax"
.globl main
main:
  # Return the value of the maximum element in the array of non-negative numbers.

  lui  a0, %hi(size)
  lw a0, %lo(size)(a0)
  # now a0 has thearrSize
  bge zero, a0, .exit

.preheader:
  # a1 has the %hi of &arr[0]
  lui  a1, %hi(arr)
  # a0 has the byte offset of next elemement
  # from &arr[0] plus the %hi(arr[0])
  # traverse array from right to left, so start
  # (size - 1) * 4 + %hi(&arr[0])
  addi a0, a0, -1
  slli a0, a0, 2
  add a0, a0, a1
  # a2 stores max so far
  addi a2, zero, -1

.loop:
  # load the value of next element in a3
  lw a3, %lo(arr)(a0)

  # update maximum
  bge a2, a3, .loopexit

.update:
  add a2, a3, zero
  # jump to next iteration if there is an element to the right

.loopexit:
  addi a0, a0, -4
  bltu a0, a1, .exit
  j .loop

.exit:
  lui  a0, %hi(__dataOutTop)
  sw a2, %lo(__dataOutTop)(a0)
  j _end

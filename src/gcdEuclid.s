# the remainder opcode requires the "M" extension
.attribute arch, "rv32im"

.section .text, "ax"
.globl main
# Euclid's algorithm to calculate gcd of two numbers b (bigger) and s (smaller) (assume b > = s):
#  while (s != 0) {
#    r = b mod s; // b = q * s + r
#    b = s;
#    s = r;
#  }
#  return b;
main:
  # The input data, b and s are passed in array. The 0th element is b, the 1st elemnt is s.
  lui  a0, %hi(arr)
  # load b into a1
  lw a1, %lo(arr)(a0)
  # load s into a2
  lw a2, %lo(arr + 4)(a0)

.loop:
  rem a3, a1, a2
  add a1, a2, zero
  add a2, a3, zero
  beq a2, zero, .exit
  j .loop

.exit:
  lui  a0, %hi(__dataOutTop)
  sw a1, %lo(__dataOutTop)(a0)
  j _end


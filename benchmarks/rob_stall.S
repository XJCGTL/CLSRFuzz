.section .text
.globl _start
_start:
  li   t0, 1
  li   t1, 1234567
  li   t2, 0
  li   t3, 2000
loop_mul:
  mul  t0, t0, t1
  add  t0, t0, t1
  xor  t0, t0, t1
  addi t2, t2, 1
  blt  t2, t3, loop_mul
  j    done
done:
  wfi

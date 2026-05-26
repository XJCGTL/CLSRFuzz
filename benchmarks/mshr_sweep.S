.section .text
.globl _start
_start:
  la   t0, data_base
  li   t1, 0
  li   t2, 256
loop_load:
  lw   t3, 0(t0)
  addi t0, t0, 4096
  addi t1, t1, 1
  blt  t1, t2, loop_load
  j    done
done:
  wfi

.section .bss
.align 12
data_base:
  .space 1048576

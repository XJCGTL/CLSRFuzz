.section .text
.globl _start
_start:
  la   t0, data_base
  li   t1, 0
  # 512 mixed load/store iterations target deep LSQ pressure in simulation.
  li   t2, 512
loop_lsq:
  lw   t3, 0(t0)
  sw   t3, 64(t0)
  addi t0, t0, 64
  addi t1, t1, 1
  blt  t1, t2, loop_lsq
  j    done
done:
  wfi

.section .bss
.align 6
data_base:
  .space 65536

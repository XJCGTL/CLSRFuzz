.section .text
.globl _start
_start:
  li t0, 0
  # 4096 alternating branches generate enough unique history to pressure BTB entries.
  li t1, 4096
loop_branch:
  addi t0, t0, 1
  andi t2, t0, 1
  beqz t2, L0
  j L1
L0:
  nop
L1:
  blt t0, t1, loop_branch
  j done
done:
  wfi

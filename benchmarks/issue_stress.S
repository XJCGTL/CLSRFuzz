.section .text
.globl _start
_start:
  # Prime initial values reduce short, repeating arithmetic cycles in stress loops.
  li t0, 3
  li t1, 5
  li t2, 7
  li t3, 11
  # 2000 iterations keep back-end ports continuously busy for measurable pressure.
  li t4, 2000
  li t5, 0
loop_issue:
  mul t0, t0, t1
  mul t2, t2, t3
  add t0, t0, t2
  xor t1, t1, t0
  addi t5, t5, 1
  blt t5, t4, loop_issue
  j done
done:
  wfi

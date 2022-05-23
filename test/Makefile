o:
	llvm-mc-13 -filetype=obj -triple=riscv32 main.s -o main.o -g
	llvm-mc-13 -filetype=obj -triple=riscv32 startup.s -o startup.o -g
	llvm-mc-13 -filetype=obj -triple=riscv32 dataIn.s -o dataIn.o -g

elf: o
	ld.lld-13 main.o startup.o dataIn.o -o test.elf -x riscv32.lds

qemu: elf
	qemu-system-riscv32 -machine virt -s -S -nographic -kernel test.elf -bios none &

gdbDebug: qemu
	gdb-multiarch test.elf --command=gdbDebug.gdb
	pkill qemu-system-ris

gdbRun: qemu
	gdb-multiarch test.elf --command=gdbRun.gdb -iex 'set pagination off' --batch
	pkill qemu-system-ris
	exit 0

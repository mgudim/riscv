runTests:
	pytest test -v -s

clean:
	rm -rf test/out

# clang-13 --target=riscv32 -c -O2 -S test.c -o test.s

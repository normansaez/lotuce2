FLAGS = -Wall -g -Wextra
LIB = -lrt
OPT = -D_XOPEN_SOURCE=700

all:build
	@echo "Finish"
build:
	@echo "Building"
	g++ $(FLAGS) $(OPT) -o cov-daemon cov-daemon.cpp $(LIB)
install:
	@echo "Installing"
clean:
	@echo "Cleaning"
	rm -fr cov-daemon

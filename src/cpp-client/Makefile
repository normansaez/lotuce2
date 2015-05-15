FLAGS = -Wall -g -Wextra
LIB = -lrt
OPT = -D_XOPEN_SOURCE=700
SRC_LIB= -I/opt/darc/include/
all:build
	@echo "Finish"
build:
	@echo "Building"
	g++ $(FLAGS) $(OPT) -o cov-daemon cov-daemon.cpp $(LIB)
	g++ $(FLAGS) $(OPT) $(SRC_LIB) -o client client.cpp $(LIB)
install:
	@echo "Installing"
clean:
	@echo "Cleaning"
	rm -fr cov-daemon

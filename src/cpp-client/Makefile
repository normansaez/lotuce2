COMPILER = g++
FLAGS = -Wall -g -Wextra
LIB = -lrt
OPT = -D_XOPEN_SOURCE=700
SRC_LIB= -I/opt/darc/include/
all:build
	@echo "Finish"
build:
	@echo "Building"
#	$(COMPILER) $(FLAGS) $(OPT) -o cov-daemon cov-daemon.cpp $(LIB)
#	$(COMPILER) $(FLAGS) $(OPT) $(SRC_LIB) -fpermissive -o client client.cpp $(LIB)
	g++ -c -O2 -Wall -Wno-unused -fexceptions  -D__OMNIORB4__ -I../../../stub -D_REENTRANT -I. -I. -I../../../include -I../../../include -I/opt/darc/include/ -D__OSVERSION__=2 -D__linux__ -D__x86_64__ -o client.o client.cpp
#	g++ -o client -O2 -Wall -Wno-unused -fexceptions -L../../../lib -L../../../lib client.o ../../../stub/echoSK.o -lomniORB4 -lomnithread -lpthread
	g++ -o client -O2 -Wall -Wno-unused -fexceptions -L../../../lib -L../../../lib client.o -lomniORB4 -lomnithread -lpthread
install:
	@echo "Installing"
clean:
	@echo "Cleaning"
	rm -fr cov-daemon
	rm -fr client

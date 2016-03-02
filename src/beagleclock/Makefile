CFLAGS+=-Wall -Werror
LDLIBS+= -lpthread -lprussdrv
TARGET=clock


all: $(TARGET).bin $(TARGET) 

clean:
	rm -f $(TARGET) *.o *.bin

$(TARGET).bin: $(TARGET).p
	pasm -b $^

$(TARGET): $(TARGET).o

run:
	./$(TARGET)

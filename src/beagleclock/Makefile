CFLAGS+=-Wall -Werror
LDLIBS+= -lpthread -lprussdrv
TARGET=clock


all: $(TARGET).bin 

clean:
	rm -f $(TARGET) *.o *.bin

$(TARGET).bin: $(TARGET).p
	pasm -b $^


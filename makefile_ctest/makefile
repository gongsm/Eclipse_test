CC = gcc
CFLAGS = $(CFLAGS_COMPILER) $(CFLAGS_EXTRA)  $(CFLAGS_DEBUG) \
         $(CFLAGS_OPTIM) $(CFLAGS_VERBOSE) $(CFLAGS_DEFINE) \
         $(CFLAGS_INCLUDE) $(CFLAGS_EXTRA)
CFLAGS_DEBUG = -g3
CFLAGS_VERBOSE  = -Wall
CFLAGS_COMPILER = -O0   -fmessage-length=0 
CFLAGS_INCLUDE = -I./include
LD = ld
SRC_FILE_PARTH = ./src
SRC_FILE = $(notdir ${wildcard $(patsubst %, %/*.c, $(SRC_FILE_PARTH))})
SRC_FILE_OBJ = $(patsubst %.c, %.o, $(SRC_FILE))
OBJS = main.o queue.o
vpath %.c ./src
all: hello libServer.a
libServer.a: queue.o
	ar -r libServer.a @filelist.lst
hello: $(SRC_FILE_OBJ) 
	$(CC) -o $@  $^
%.o:%.c
	$(CC) $(CFLAGS) -o  $@ -c $<

clean:
	rm *.o *.exe *.a

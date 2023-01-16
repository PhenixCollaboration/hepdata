CC = g++ 

INCLUDES = 

CFLAGS = -g -Wall -std=c++11 $(INCLUDES)

LIBDIR = 

LIBS = 

EXECUTABLES = yaml_data

all: $(EXECUTABLES)

.SUFFIXES: .c .o
.c.o:
	$(CC) $(CFLAGS) -c $*.c

yaml_data: yaml_data.o
	$(CC) $(CFLAGS) -o yaml_data yaml_data.o $(LIBS)

#make clean will rid your directory of the executable,& object files
clean:
	rm $(EXECUTABLES) *.o



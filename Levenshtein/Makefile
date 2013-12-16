CXXFLAGS =	-O3 -march=native -mtune=native -g -Wall -ffast-math -fmessage-length=0
LDFLAGS =  -O3 -march=native -mtune=native -largtable2 -static

OBJS =		levenshtein.o 
HEADERS =	*.h
LIBS =

default: all

levenshtein : levenshtein.o
	$(CXX) $(CXXFLAGS) levenshtein.o $(LDFLAGS) -o levenshtein

%.o : %.cpp *.h Makefile
	@echo "***" $< "***"
	$(CXX) $(CXXFLAGS) -c $< -o $@  

.PHONY : all clean
all:	levenshtein

clean:
	rm -f $(OBJS) $(TARGET)
	

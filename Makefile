.PHONY: clean all

# python version
VER ?= 3.8

all: mi.so

clean:
	rm -rf *.so *.o

mi.o: mi1.cpp 
	g++ -fPIC -c $$(python${VER}-config  --includes) -o mi.o mi1.cpp

mi.so: mi.o
	g++ $$(python${VER}-config --ldflags) -lpython${VER} -shared mi.o -o libmi.so

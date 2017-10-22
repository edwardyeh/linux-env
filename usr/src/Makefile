######## User Define ###########################################################
export SRC_DIR = ../src
export INC_DIR = ../include
export LIB_DIR = ../lib64
export BIN_DIR = ../bin
export CC      = gcc
export CFLAGS  = -Wall -m64 -I$(INC_DIR) -L$(LIB_DIR) 
export DEBUG   = -g
######## Version Info ##########################################################
export IMAGE_VER = 1.0.0
################################################################################

.PHONY: all image bmp2yuv precision_calc

IMAGE_MVER=`echo $(IMAGE_VER) | sed 's/\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\1/g'`

all: image bmp2yuv precision_calc

image:
	$(CC) $(CFLAGS) -fpic -c $(SRC_DIR)/image.c
	\rm -rf $(LIB_DIR)/libimage.a
	ar crvs $(LIB_DIR)/libimage.a image.o
	\rm -rf $(LIB_DIR)/libimage.so.$(IMAGE_MVER).*
	gcc -shared -Wl,-soname,libimage.so.$(IMAGE_MVER) -o $(LIB_DIR)/libimage.so.$(IMAGE_VER) image.o
	\rm -rf image.o
	`cd $(LIB_DIR); echo $(IMAGE_VER) | sed 's/\([0-9]\)\..*$$/\1/g' | xargs -i ln -sf libimage.so.$(IMAGE_VER) libimage.so.{}`

bmp2yuv:
	$(CC) $(CFLAGS) -o $(BIN_DIR)/bmp2yuv bmp2yuv.c -limage

precision_calc:
	$(CC) $(CFLAGS) -o $(BIN_DIR)/precision_calc precision_calc.c 

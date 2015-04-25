// +FHDR-----------------------------------------------------------------------
// Copyright (c) 2013-2014 Hsin-Hsien Yeh (Edward Yeh). All rights reserved.
// Filename        : bmp2yuv.c
// Version         : $Revision: $
// Last Modified On: $Date: $
// Last Modified By: $Author: $
//                   
// File Description: BMP to YUV tool
// ----------------------------------------------------------------------------
// Reuse Issues    : 
// Parameters      : 
//                   
// Abbreviations   : 
// Release History : 
// ----------------------------------------------------------------------------
// Author          : Edward Yeh
// Created On      : Sun, Nov 30, 2014  8:40:02 PM
// Format          : 
// ----------------------------------------------------------------------------
// $Log: bmp2yuv.c,v $
// -FHDR-----------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "image.h"

int main (int argc, char* argv[])
{
    FILE *dst_fp;               // Destination image file pointer

    unsigned int x_st;          // Horizontal scan start position
    unsigned int y_st;          // Vertical scan start position
    unsigned int dst_w;         // Destination image width
    unsigned int dst_h;         // Destination image height
    unsigned int dst_sz;        // Destination image size

    char src_fn[64];            // Source image filename
    char dst_fn[64];            // Destination image filename

    unsigned char *rgb24_img_buf;
    unsigned char *yuy2_img_buf;

    if (argc == 5) {
        x_st   = 0;
        y_st   = 0;
        dst_w  = atoi(argv[1]);
        dst_h  = atoi(argv[2]);
        dst_sz = dst_w * dst_h;
        
        strcpy(src_fn, argv[3]);
        strcpy(dst_fn, argv[4]);
    }
    else if (argc == 7) {
        x_st   = atoi(argv[1]);
        y_st   = atoi(argv[2]);
        dst_w  = atoi(argv[3]);
        dst_h  = atoi(argv[4]);
        dst_sz = dst_w * dst_h;

        strcpy(src_fn, argv[5]);
        strcpy(dst_fn, argv[6]);
    }
    else {
        printf("bmp2yuv: BMP to YUV tool.\n");
        printf("\n");
        printf("  Usage1:  bmp2yuv <x_st> <y_st> <dst_w> <dst_h> <src_fn> <dst_fn>\n");
        printf("  Usage2:  bmp2yuv <dst_w> <dst_h> <src_fn> <dst_fn>\n");
        printf("\n");
        printf("    x_st    Horizontal scan start position\n");
        printf("    y_st    Vertical scan start position\n");
        printf("    dst_w   Destination image width\n");
        printf("    dst_h   Destination image height\n");
        printf("    src_fn  Source image filename\n");
        printf("    dst_fn  Destination image filename\n");
        printf("\n");
        return 1;
    }

    if ((dst_fp = fopen(dst_fn, "wb")) == NULL) {
        printf("[BMP2YUV] Cannot not create destination image file.\n");        
        return 1;
    }

    rgb24_img_buf = (unsigned char*)malloc(sizeof(char)*dst_sz*3); 
    yuy2_img_buf  = (unsigned char*)malloc(sizeof(char)*dst_sz*2);
    ReadBMP(src_fn, x_st, x_st+dst_w, y_st, y_st+dst_h, rgb24_img_buf);
    RGB24toYUY2(rgb24_img_buf, yuy2_img_buf, dst_w, dst_h);
    fwrite(yuy2_img_buf, sizeof(char), dst_sz*2, dst_fp);
    
    free(rgb24_img_buf);
    free(yuy2_img_buf);
    fclose(dst_fp);

    return 0;
}

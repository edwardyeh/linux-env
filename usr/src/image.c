// +FHDR-----------------------------------------------------------------------
// Copyright (c) 2013-2014 Hsin-Hsien Yeh (Edward Yeh). All rights reserved.
// Filename        : image.c
// Version         : $Revision: $
// Last Modified On: $Date: $
// Last Modified By: $Author: $
//                   
// File Description: Image process function library
// ----------------------------------------------------------------------------
// Reuse Issues    : 
// Parameters      : 
//                   
// Abbreviations   : 
// Release History : 
// ----------------------------------------------------------------------------
// Author          : Edward Yeh
// Created On      : Sun, Nov 30, 2014  2:38:35 PM
// Format          : 
// ----------------------------------------------------------------------------
// $Log: image.c,v $
// -FHDR-----------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "image.h"

#ifndef WIN32
static inline int clip (int x) { return ((x < 0) ? 0 : ((x > 255) ? 255 : x)); }
#endif  //WIN32

/*
*******************************************************************************
*  Function name: ReadBMP
*
*  Description: Read BMP file and utput RGB24 raw data
*
*  Input:  [1] unsigned char *img_fn      : source image filename
*          [2] unsigned int  x_st         : Horizontal scan start position
*          [3] unsigned int  x_ed         : Horizontal scan end position
*          [4] unsigned int  y_st         : Vertical scan start position
*          [5] unisnged int  y_ed         : Vertical scan end position
*
*  Output: [1] unsigned char *out_img_buf : output image buffer
*
*  Return: 0- Normal finish, 1- Process error.
*
*******************************************************************************
*/
int ReadBMP (char *img_fn, 
             unsigned int x_st,
             unsigned int x_ed,
             unsigned int y_st,
             unsigned int y_ed, 
             unsigned char *out_img_buf)

{
    FILE *fpSrc = NULL;             // Source file pointer
    unsigned int img_w;             // Image width
    unsigned int img_h;             // Image height
    unsigned int rgb_raw_off;       // Raw data offset in the BMP file
    unsigned int ln_end_off;        // Line end offset
    unsigned char *pBuf = NULL;     // Temp buffer pointer
    unsigned char *pOut = NULL;     // Output buffer pointer    
    unsigned int x, y;
    unsigned int y_inv;

    if ((fpSrc = fopen(img_fn, "rb+")) == NULL) {
        printf("[ReadBMP] Cannot open source image file.\n");
        return 1;
    }

    fseek(fpSrc, 10, SEEK_SET);
    fread(&rgb_raw_off, sizeof(int), 1, fpSrc);

    fseek(fpSrc, 18, SEEK_SET);
    fread(&img_w, sizeof(int), 1, fpSrc);
    fread(&img_h, sizeof(int), 1, fpSrc);
    ln_end_off = img_w % 4;

    fseek(fpSrc, rgb_raw_off, SEEK_SET);

    pBuf = (unsigned char*)malloc(sizeof(char)*(img_w*img_h*3+ln_end_off*img_h));
    if (pBuf == NULL) {
        printf("[ReadBMP] Cannot allocate the temporary buffer.\n");
        return 1;
    }

    pOut = out_img_buf;
    fread(pBuf, sizeof(char), (img_w*img_h*3+ln_end_off*img_h), fpSrc);

    for (y = y_st; y < y_ed; y++) {
        for (x = x_st; x < x_ed; x++) {
            y_inv = (y_ed - 1) - y;
            *(pOut+3*(img_w*y_inv+x)+2) = *(pBuf+3*(img_w*y+x)+(ln_end_off*y)+2);   // R
            *(pOut+3*(img_w*y_inv+x)+1) = *(pBuf+3*(img_w*y+x)+(ln_end_off*y)+1);   // G
            *(pOut+3*(img_w*y_inv+x)+0) = *(pBuf+3*(img_w*y+x)+(ln_end_off*y)+0);   // B
        }
    }

    free(pBuf);
    fclose(fpSrc);

    return 0;
} //int ReadBMP (

/*
*******************************************************************************
*  Function name: RGB24toYUY2
*
*  Description: Convert RGB24 format to YUY2 (Y0 U0 Y1 V1)
*
*  Input:  [1] unsigned char *in_buf    : source image buffer
*          [3] int img_w                : image width
*          [4] int img_h                : image height 
*
*  Output: [1] unsigned char *out_buf   : destination image buffer
*
*  Return: 0- Normal finish, 1- Process error.
*
*******************************************************************************
*/
int RGB24toYUY2 (unsigned char *in_buf, unsigned char *out_buf, int img_w, int img_h)
{
    int i, j;
    int R, G, B;
    int Y, U, V;
    int size3;

    size3 = img_w * img_h * 3;

    for (i = 0, j = 0; i < size3; i += 3) {
        R = (int)in_buf[i+2];
        G = (int)in_buf[i+1];
        B = (int)in_buf[i];

        Y = (( 77 * R + 150 * G +  29 * B) >> 8);
        U = ((-43 * R -  85 * G + 128 * B) >> 8) + 128;
        V = ((128 * R - 107 * G -  21 * B) >> 8) + 128;

        out_buf[j++] = (unsigned char)clip(Y);

        if ((i & 0x1) == 0)
            out_buf[j++] = (unsigned char)clip(U);
        else
            out_buf[j++] = (unsigned char)clip(V);
    }

    return 0;
} //int RGB24toYUV2 (


// +FHDR-----------------------------------------------------------------------
// Copyright (c) 2013-2014 Hsin-Hsien Yeh (Edward Yeh). All rights reserved.
// Filename        : image.h
// Version         : $Revision: $
// Last Modified On: $Date: $
// Last Modified By: $Author: $
//                   
// File Description: 
// ----------------------------------------------------------------------------
// Reuse Issues    : 
// Parameters      : 
//                   
// Abbreviations   : 
// Release History : 
// ----------------------------------------------------------------------------
// Author          : Edward Yeh
// Created On      : Sun, Nov 30, 2014  2:39:28 PM
// Format          : 
// ----------------------------------------------------------------------------
// $Log: image.h,v $
// -FHDR-----------------------------------------------------------------------

#ifndef _IMAGE_EY_
#define _IMAGE_EY_

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
             unsigned char *out_img_buf);

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
int RGB24toYUY2 (unsigned char *in_buf, unsigned char *out_buf, int img_w, int img_h);

#endif

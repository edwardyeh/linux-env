// +FHDR-----------------------------------------------------------------------
// Copyright (c) 2017 Hsin-Hsien Yeh (Edward Yeh). All rights reserved.
// Filename        : precision_calc.c
// File Description: Precision calculation for the fix-point number
// ----------------------------------------------------------------------------
// Reuse Issues    : 
// Abbreviations   : 
// Release History : 
// ----------------------------------------------------------------------------
// Author          : Edward Yeh
// Created On      : Tue Sep 26 00:23:46 CST 2017
// Format          : C/C++
// ----------------------------------------------------------------------------
// $Log: precision_calc.c,v $
// -FHDR-----------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static inline void result_display (int frac, double num, double err_rate, int fix)
{
    printf("Frac_bits: %2d, val: %f, error_rate: %f, fix_point: %d\n", frac, num, err_rate, fix);
};

static inline void usage ()
{
    printf("Usage: precision_calc <FP_num> <frac_bit>\n\n");
    printf("Precision calculation for the float-point to fix-point conversion.\n\n");
    printf("Arguments:\n");
    printf("  FP_num        Float-point number which to be converted.\n");
    printf("  frac_bit      Fraction bits to represent the fix-point number.\n\n");
}

int main (int argc, char* argv[])
{
    double  fp_num, num, min_num, err_rate;
    int     frac_bit, frac, fix, min_fix, shift;

    if (argc != 3) {
        usage();
        return 1;
    }

    fp_num   = atof(argv[1]);
    frac_bit = atoi(argv[2]);

    for (frac = 1; frac <= frac_bit; frac++) {
        num = 1.0 / (1 << frac);
        if (num == fp_num)
            result_display(frac, num, 0.0, 1);
        else {
            min_num = num;
            min_fix = 1;

            for (fix = 1; fix < (1 << frac); fix++) {
                num = 0;

                for (shift = 0; shift < frac; shift++) {
                    if ((fix >> shift) & 0x1)
                        num += 1.0 / (1 << (frac - shift));
                }

                if (fabs(fp_num-num) < fabs(fp_num-min_num)) {
                    min_num = num;
                    min_fix = fix;
                }
                else if (num > fp_num)
                    break;
            }

            err_rate = (fp_num - min_num) / fp_num;
            result_display(frac, min_num, err_rate, min_fix);
        }
    }

    return 0;
}

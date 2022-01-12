#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## +FHDR=======================================================================
## Copyright (c) 2022 Hsin-Hsien Yeh (Edward Yeh).
## All rights reserved.
## ----------------------------------------------------------------------------
## Filename         : cfg2xls.py
## File Description : Programming reference table convertor
## ----------------------------------------------------------------------------
## Author           : Edward Yeh
## Created On       : Wed 12 Jan 2022 02:34:24 AM CST
## Format           : Python module
## ----------------------------------------------------------------------------
## Reuse Issues     : 
## ----------------------------------------------------------------------------
## Release History  : 
## -FHDR=======================================================================

import os
import shutil
import argparse
import textwrap
import openpyxl

from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.styles import Border
from openpyxl.styles import Side
from openpyxl.styles import Alignment

### Class Definition ###

class RegisterTable:
    """Programming register table"""

    def __init__(self, reg_fn: str, table_type: str, is_debug: bool):
    #{{{
        self.is_debug = is_debug
        self.comment_sign = '#'
        self.reg_table = {}     # {addr1: reg_list1, addr2: reg_list2, ...}
        self.pat_list  = []

        if table_type == 'cfg':
            self.cfg_reg_parser(reg_fn)
        elif table_type == 'xls':
            self.xls_reg_parser(reg_fn)
        else:
            raise TypeError("Unsupport register table type ({})".format(table_type))
    #}}}

    def cfg_reg_parser(self, reg_fn: str):
        """Parse co nfig type register table"""  #{{{

        with open(reg_fn, 'r') as f:
            # reg_list = [type, title, tag, reg1, reg2, ...]
            reg_list = [None, None, None] 
            reg_act = False
            reg_addr = 0

            line = f.readline()
            while line:
                toks = line.split()
                if len(toks):
                    if toks[0] == 'H:' or toks[0] == 'A:' or toks[0] == 'T:':
                        if reg_act:
                            self.reg_table[reg_addr] = reg_list
                            reg_list = [None, None, None]
                        if toks[0] == 'T:':
                            reg_act = False
                            reg_list[2] = toks[1]
                        else:
                            reg_act = True
                            reg_addr = self.get_int_val(toks[1])
                            reg_list[0] = toks[0]
                            if len(toks) > 2:
                                reg_list[1] = ' '.join(toks[2:]).strip("\"\'")
                    else:
                        # reg = [reg_name, msb, lsb, init_value, comment, row_idx]
                        reg = [toks[0].upper(), 
                               int(toks[1]), 
                               int(toks[2]), 
                               self.get_int_val(toks[3])]
                        if len(toks) > 4:
                            reg.append(' '.join(toks[4:]).strip("\"\'"))
                        else:
                            reg.append(None)
                        reg.append(None)    # row_idx is no use in this mode
                        reg_list.append(reg)
                line = f.readline()

            if reg_act:
                self.reg_table[reg_addr] = reg_list

        if self.is_debug:
            self.show_reg_table("=== REG TABLE PARSER ===")
    #}}}

    def xls_reg_parser(self, reg_fn: str):
        """Parse excel type register table"""  #{{{

        wb = openpyxl.load_workbook(reg_fn)
        ws = wb.worksheets[0]

        # reg_list = [type, title, tag, reg1, reg2, ...]
        reg_list = [None, None, None] 
        reg_act = False
        reg_addr = 0

        addr_col = tuple(ws.iter_cols(1, 1, None, None, True))[0]
        for i in range(addr_col.index('ADDR')+1, len(addr_col)):
            row_idx = i + 1
            val = addr_col[i]
            if val is not None:
                val = str(val)
                if reg_act:
                    self.reg_table[reg_addr] = reg_list
                if val == 'none':
                    break
                else:
                    reg_addr = int(val, 16)
                    if ws.cell(row_idx, 1).font.__getattr__('color'):
                        reg_list = ['H:', None, None]
                    else:
                        reg_list = ['A:', None, None]
                    title = ws.cell(row_idx, 2).value
                    if title is not None:
                        reg_list[1] = str(title)

            reg_val = self.get_int_val(str(ws.cell(row_idx, 3).value))

            bits = str(ws.cell(row_idx, 4).value).split('_')
            if len(bits) > 1:
                msb, lsb = int(bits[0]), int(bits[1])
            else:
                msb = lsb = int(bits[0])

            toks = str(ws.cell(row_idx, 5).value).split();
            reg_name = toks[0].upper()
            comment = None if len(toks) == 1 else ' '.join(toks[1:])

            # reg = [reg_name, msb, lsb, init_value, comment, row_idx]
            reg_list.append([reg_name, msb, lsb, reg_val, comment, row_idx])
            reg_act = True

        wb.close()

        if self.is_debug:
            self.show_reg_table("=== XLS TABLE PARSER ===")
    #}}}

    def cfg_dump(self, is_export: bool):
        """Dump config text""" #{{{

        pass
    #}}}

    def xls_dump(self, is_export: bool):
        """Dump excel file""" #{{{

        ### initial workbook ###

        wb = openpyxl.Workbook()
        ws = wb.worksheets[0]

        grey_font = Font(color='808080')
        orange_fill = PatternFill(fill_type='solid', start_color='ffcc99')
        yellow_fill = PatternFill(fill_type='solid', start_color='ffffcc')
        green_fill = PatternFill(fill_type='solid', start_color='92d050')
        violet_fill = PatternFill(fill_type='solid', start_color='e6ccff')
        grey_fill = PatternFill(fill_type='solid', start_color='dddddd')
        thin_side = Side(border_style='thin', color='000000')
        around_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
        left_top_align = Alignment(horizontal='left', vertical='top')
        left_center_align = Alignment(horizontal='left', vertical='center')
        center_top_align = Alignment(horizontal='center', vertical='top')
        center_center_align = Alignment(horizontal='center', vertical='center')
        right_top_align = Alignment(horizontal='right', vertical='top')
        right_center_align = Alignment(horizontal='right', vertical='center')

        ws.column_dimensions['A'].width = 15.46
        ws.column_dimensions['B'].width = 41.23
        ws.column_dimensions['C'].width = 10.31
        ws.column_dimensions['D'].width = 10.31
        ws.column_dimensions[chr(65+4)].width = 41.23

        for row in ws['A1:D5']:
            for cell in row:
                cell.border = around_border

        values = ['chip', 'eng.', 'date']
        for row, val in enumerate(values, start=2):
            cell = ws.cell(row, 1, val)
            cell.fill = orange_fill
            cell.alignment = center_center_align

        values = ['Number', 'FileName', 'Metion1', 'Metion2', 'PatternStatus']
        for row, val in enumerate(values, start=1):
            cell = ws.cell(row, 5, val)
            cell.fill = yellow_fill
            cell.border = around_border
            cell.alignment = left_center_align

        cell = ws.cell(6, 1, 'ADDR')
        cell.fill = green_fill
        cell.border = around_border
        cell.alignment = center_center_align

        cell = ws.cell(6, 2, 'Register')
        cell.fill = green_fill
        cell.border = around_border
        cell.alignment = left_center_align

        cell = ws.cell(6, 3, 'INI')
        cell.fill = green_fill
        cell.border = around_border
        cell.alignment = right_center_align

        cell = ws.cell(6, 4, 'Bits')
        cell.fill = green_fill
        cell.border = around_border
        cell.alignment = right_center_align

        cell = ws.cell(6, 5, 'Member')
        cell.fill = green_fill
        cell.border = around_border
        cell.alignment = left_center_align

        for row in ws['F1:AMJ1']:
            for cell in row:
                cell.fill = violet_fill
                cell.border = around_border
                cell.alignment = center_center_align

        for row in ws['F2:AMJ2']:
            for cell in row:
                cell.fill = violet_fill
                cell.border = around_border
                cell.alignment = center_center_align

        for row in ws['F3:AMJ3']:
            for cell in row:
                cell.border = around_border
                cell.alignment = center_center_align

        for row in ws['F4:AMJ4']:
            for cell in row:
                cell.border = around_border
                cell.alignment = center_center_align

        for row in ws['F5:AMJ5']:
            for cell in row:
                cell.border = around_border
                cell.alignment = center_center_align

        for row in ws['F6:AMJ6']:
            for cell in row:
                cell.fill = green_fill 
                cell.border = around_border
                cell.alignment = center_center_align

        if is_export:
            ws.cell(1, 6, 6)
            ws.cell(2, 6, 'PAT-1')

        ### dump register ###

        row_st = row_ed = 7

        for addr, reg_list in self.reg_table.items():
            is_first = True
            cell_font = grey_font if reg_list[0] == 'H:' else Font()

            for reg in reg_list[3:]:
                cell_fill = yellow_fill if is_first else PatternFill()

                row_range = ''.join(['A', str(row_ed), ':AMJ', str(row_ed)])
                for row in ws[row_range]:
                    for cell in row:
                        cell.border = around_border
                        cell.fill = cell_fill
                        cell.font = cell_font
                        cell.alignment = center_center_align

                if is_first:
                    cell = ws.cell(row_ed, 1, hex(addr))
                    cell.alignment = center_top_align

                    cell = ws.cell(row_ed, 2, reg_list[1])
                    cell.alignment = left_top_align

                cell = ws.cell(row_ed, 3, hex(reg[3]))
                cell.alignment = right_top_align

                if is_export:
                    ws.cell(row_ed, 6, hex(reg[3]).upper()[2:])

                if reg[1] == reg[2]:
                    cell = ws.cell(row_ed, 4, str(reg[1]))
                else:
                    cell = ws.cell(row_ed, 4, '_'.join([str(reg[1]), str(reg[2])]))
                cell.alignment = right_top_align

                if reg[0] == 'RESERVED':
                    cell = ws.cell(row_ed, 5, reg[0].lower())
                else:
                    comments = [] if reg[4] == None else reg[4].split(',')
                    cell = ws.cell(row_ed, 5, '\n'.join([reg[0]] + comments))
                cell.alignment = left_top_align
                row_ed += 1
                is_first = False

        row_range = ''.join(['A', str(row_ed), ':AMJ', str(row_ed)])
        for row in ws[row_range]:
            for cell in row:
                cell.border = around_border
                cell.fill = grey_fill
                cell.alignment = center_top_align
        ws.cell(row_ed, 1, 'none')
        row_ed += 1

        wb.save("table_dump.xlsx")
        wb.close()
    #}}}

    def get_int_val(self, str_val: str) -> int:
        """Convert string to integer (with HEX check)""" #{{{
        if str_val.startswith('0x') or str_val.startswith('0X') :
            return int(str_val, 16)
        else:
            return int(str_val)
    #}}}

    def show_reg_table(self, comment : str):
        """Show register table""" #{{{
        print(comment)
        for addr, reg_list in self.reg_table.items():
            print("{}".format([hex(addr)] + reg_list[0:3]))
            for reg in reg_list[3:]:
                print("  {}".format(reg))
        print()
    #}}}

### Main Function ###

def main(is_debug=False):
    """Main function""" #{{{
    parser = argparse.ArgumentParser(
            usage='%(prog)s [options]',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''
                Programming Register Table converter.

                  config text to excel is default mode.
                '''))

    parser.add_argument('-i', dest='is_inverse', action='store_true', 
                              help='inverse mode (excel to config text)')
    parser.add_argument('-e', dest='is_export', action='store_true', 
                              help='export default setting')
    parser.add_argument('file', help='file name') 

    args = parser.parse_args()

    ## Parser register table & dump
    pat_list = None
    if args.is_inverse:
        pat_list = RegisterTable(args.file, 'xls', is_debug)
    else:
        pat_list = RegisterTable(args.file, 'cfg', is_debug)
        pat_list.xls_dump(args.is_export)
#}}}

if __name__ == '__main__':
    main(True)
else:
    pass

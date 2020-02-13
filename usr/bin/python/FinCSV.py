#! /bin/python
## +FHDR=======================================================================
## Copyright (c) 2020 Hsin-Hsien Yeh (Edward Yeh).
## All rights reserved.
## ----------------------------------------------------------------------------
## Filename         : FinCSV.py
## File Description : 
## ----------------------------------------------------------------------------
## Author           : Edward Yeh
## Created On       : Thu, Feb  6, 2020 10:31:53 PM
## Format           : Python script
## ----------------------------------------------------------------------------
## Reuse Issues     : 
## Release History  : 
## -FHDR=======================================================================

import sys
import csv
import re

### Class Definition ###

class FinCSV:
    """Financial CSV manager"""
    def __init__ (self):
        self.header = []
        self.trans = []

    def get_header (self, fn: str, enc: str, start_ln: int) -> list:
        """Get transaction title"""
        with open(fn, encoding = enc) as f:
            f_csv = csv.reader(f)
            for i in range(0, start_ln - 1):
                next(f_csv)     # discard redundant line
            header = next(f_csv)
            return header

    def get_trans (self, fn: str, enc: str, start_ln: int) -> list:
        """Get transactions"""
        with open(fn, encoding = enc) as f:
            f_csv = csv.reader(f)
            for i in range(0, start_ln - 1):
                next(f_csv)     # discard redundant & header line
            trans = []
            for line in f_csv:
                trans.append(line)
            return trans 

    def import_header (self, fn: str, enc: str, start_ln: int):
        """Import header"""
        self.header = self.get_header(fn, enc, start_ln)

    def import_trans (self, fn: str, enc: str, start_ln: int):
        """Import transations"""
        self.trans = self.get_trans(fn, enc, start_ln)

    def dump_csv (self, fn: str, enc: str):
        """Dump financial CSV"""
        with open(fn, 'w', encoding = enc) as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.header)
            f_csv.writerows(self.trans)

class GnuCashCSV (FinCSV):
    """Financial CSV manager for GnuCash"""
    def __init__ (self):
        FinCSV.__init__(self)
        self.header = ['Date', 'Transaction ID', 'Number', 'Description', 
                       'Notes', 'Commodity/Currency', 'Void Reason', 'Action', 
                       'Memo', 'Full Account Name', 'Account Name', 
                       'Amount With Sym', 'Amount Num.', 'Reconcile', 
                       'Reconcile Date', 'Rate/Price']

    def add_rev_exp_bc (self, ln_no: int, src_trans: list) -> int:
        """Add a revenue or expenditure to table """
        regex = re.compile(r'\[\{.*\}\]')
        tran_dst = []
        tran_src = src_trans[ln_no]
        tran_split = regex.search(tran_src[10])
        tran_dst.append(tran_src[1].split(' ')[0].replace('-', '/'))  # Date

        for i in range(0, 2): 
            tran_dst.append('')

        tran_dst.append(tran_src[3])  # Description

        if (tran_split):  # Note
            note = tran_split.group()
            tran_dst.append(note[2:len(note)-2])
        else:
            note = ''
            tran_dst.append(tran_src[10])

        tran_dst.append('CURRENCY::' + tran_src[5])  # Currency

        for i in range(0, 3): 
            tran_dst.append('')

        tran_dst.append(tran_src[9])  # Account

        for i in range(0, 2): 
            tran_dst.append('')

        if (tran_split):  # Amount
            tran_dst.append('')
        else:
            tran_dst.append(tran_src[4])

        tran_dst.append('n')         # Reconcile
        tran_dst.append('')
        tran_dst.append(tran_src[6])  # Rate
        gc_idx = len(self.trans)
        self.trans.append(tran_dst)

        amounts = 0.0
        while True:
            tran_dst = []
            tran_src = src_trans[ln_no]

            for i in range(0, 8):
                tran_dst.append('')

            if (tran_split):  # Memo
                tran_dst.append(tran_src[10][len(note):])
            else:
                tran_dst.append('')

            tran_dst.append(tran_src[7] + ':' + tran_src[8])  # Account

            for i in range(0, 2):
                tran_dst.append('')

            amount = float(tran_src[4])
            amounts = amounts + amount

            tran_dst.append(str(amount * -1))  # Amount
            tran_dst.append('n')               # Reconcile
            tran_dst.append('')
            tran_dst.append(tran_src[6])        # Rate
            self.trans.append(tran_dst)

            ln_no = ln_no + 1
            if (tran_split == None):
                break
            elif (len(src_trans) == ln_no):
                break
            else:
                next_split = regex.search(src_trans[ln_no][10])
                if (next_split == None):
                    break
                elif (note != next_split.group()):
                    break

        if (tran_split):
            self.trans[gc_idx][12] = str(amounts)

        return ln_no

    def add_tranf_bc (self, ln_no: int, src_trans: list):
        """Add a transfer to table """
        tran_dst = []
        tran_src = src_trans[ln_no]
        tran_dst.append(tran_src[1].split(' ')[0].replace('-', '/'))  # Date

        for i in range(0, 2): 
            tran_dst.append('')

        tran_dst.append(tran_src[3])                 # Description
        tran_dst.append(tran_src[10])                # Note
        tran_dst.append('CURRENCY::' + tran_src[5])  # Currency

        for i in range(0, 3): 
            tran_dst.append('')

        tran_dst.append(tran_src[9])  # Account

        for i in range(0, 2): 
            tran_dst.append('')

        tran_dst.append(tran_src[4])  # Amount
        tran_dst.append('n')         # Reconcile
        tran_dst.append('')
        tran_dst.append(tran_src[6])  # Rate
        self.trans.append(tran_dst)

        ln_no = ln_no + 1
        tran_dst = []
        tran_src = src_trans[ln_no]

        for i in range(0, 9):
            tran_dst.append('')

        tran_dst.append(tran_src[9])  # Account

        for i in range(0, 2):
            tran_dst.append('')

        tran_dst.append(tran_src[4])  # Amount
        tran_dst.append('n')         # Reconcile
        tran_dst.append('')
        tran_dst.append(tran_src[6])  # Rate
        self.trans.append(tran_dst)

        return ln_no + 1

    def import_bc_trans (self, fn: str):
        """Read Bluecoins CSV and convert to GnuCash CSV"""
        src_trans = self.get_trans(fn, 'UTF-8', 2)
        ln_no = 0
        while ln_no < len(src_trans):
            if src_trans[ln_no][0] == '轉帳':
                ln_no = self.add_tranf_bc(ln_no, src_trans)
            else:
                ln_no = self.add_rev_exp_bc(ln_no, src_trans)

class BluecoinsCSV (FinCSV):
    """Financial CSV manager for Bluecoins"""
    def __init__ (self):
        FinCSV.__init__(self)
        self.header = ['Type', 'Date', 'Item', 'Amount', 'Currency', 
                       'ConversionRate', 'Parent Category', 'Category', 
                       'Account Type', 'Account', 'Notes', 'Label', 'Status', 
                       'Split']

    def add_rev_exp_am (self, ln_no: int, src_trans: list) -> int:
        """Add a revenue or expenditure to table """
        tran_dst = []
        tran_src = src_trans[ln_no]

        tran_dst.append('Expense')  # Type

        date = tran_src[5]
        date =  date[4:6] + '/' + date[6:8] + '/' + date[0:4]

        time = tran_src[13]
        for i in range(len(time), 4):
            time = '0' + time
        time = time[0:2] + ':' + time[2:4]

        tran_dst.append(date + ' ' + time)  # Date
        tran_dst.append(tran_src[11])       # Item
        tran_dst.append(tran_src[2])        # Amount
        tran_dst.append('TWD')              # Currency
        tran_dst.append('1')                # ConversionRate
        tran_dst.append(tran_src[3])        # Parent Category
        tran_dst.append(tran_src[4])        # Category
        tran_dst.append('')                 # Account type
        tran_dst.append(tran_src[6])        # Account

        note = ""
        for line in tran_src[8].split(' \\n '):
            note = note + line + '\n'

        tran_dst.append(note[:len(note)-1])  # Note
        tran_dst.append('')                  # Label
        tran_dst.append('')                  # Status
        tran_dst.append('')                  # Split 
        self.trans.append(tran_dst)

        return ln_no + 1

    def import_am_trans (self, fn: str):
        """Read AndroMoney CSV and convert to Bluecoins CSV"""
        src_trans = self.get_trans(fn, 'Big5', 3)
        ln_no = 0
        while ln_no < len(src_trans):
            ln_no = self.add_rev_exp_am(ln_no, src_trans)

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print('Financial CSV Convertor\n')
        print('Usage: python FinCSV.py <type> <csv_in> <csv_out>\n')
        print('Argument:\n')
        print('  type       1: Bluecoins -> GnuCash')
        print('             2: AndroMoney -> Bluecoins')
        print('  csv_in     input CSV file name')
        print('  csv_out    output CSV file name\n')
    elif (sys.argv[1] == '1'):
        gc_csv = GnuCashCSV()
        gc_csv.import_bc_trans(sys.argv[2])
        gc_csv.dump_csv(sys.argv[3], 'UTF-8')
    elif (sys.argv[1] == '2'):
        bc_csv = BluecoinsCSV()
        bc_csv.import_am_trans(sys.argv[2])
        bc_csv.dump_csv(sys.argv[3], 'UTF-8')
    else:
        print('Error type!!!')



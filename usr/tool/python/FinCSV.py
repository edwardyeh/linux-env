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
    def __init__ (self, table = None, header_ref = None):  
    #{{{
        if header_ref == None:
            if table == None:
                self.header = []
                self.trans  = []
            else:
                self.header = table[0]
                self.trans  = table[1]
        else:
            self.header = header_ref
            if table == None:
                self.trans = []
            elif len(table[0]) != len(header_ref):
                print('[Warning] Header mismatch, discard!!!')
                self.trans = []
            else:
                self.trans = table[1]
                for i in range(0, len(header_ref)):
                    if table[0][i] != header_ref[i]:
                        print('[Warning] Header mismatch, discard!!!')
                        self.trans  = []
                        break

        self.table = [self.header, self.trans]
    #}}}

    def get_header (self, fn: str, enc: str, start_ln: int) -> list:
        """Get header from CSV"""   #{{{
        with open(fn, encoding = enc) as f:
            f_csv = csv.reader(f)
            for i in range(0, start_ln - 1):
                next(f_csv)     # discard redundant line
            return next(f_csv)
    #}}}

    def get_trans (self, fn: str, enc: str, start_ln: int) -> list:
        """Get transactions from CSV""" #{{{
        with open(fn, encoding = enc) as f:
            f_csv = csv.reader(f)
            for i in range(0, start_ln):
                next(f_csv)     # discard redundant & header line
            trans = []
            for line in f_csv:
                trans.append(line)
            return trans 
    #}}}

    def get_table (self, fn: str, enc: str, start_ln: int) -> list:
        """Get transaction table from CSV"""    #{{{
        header = self.get_header(fn, enc, start_ln)
        trans  = self.get_trans(fn, enc, start_ln)
        return [header, trans]
    #}}}

    def import_table (self, fn: str, enc: str, start_ln: int):
        """Import transaction table"""  #{{{
        self.table  = self.get_table(fn, enc, start_ln)
        self.header = self.table[0]
        self.trans  = self.table[1]
    #}}}

    def search_trans (self, index: int, content: str) -> list:
        """Return a table with specific transactions (1 line format)"""  #{{{
        trans = []
        for tran in self.trans:
            if tran[index] == content:
                trans.append(tran)
        return [self.header, trans]
    #}}}

    def del_trans (self, index: int, content: str) -> list:
        """Return a table without specific transactions (1 line format)"""  #{{{
        trans = []
        for tran in self.trans:
            if tran[index] != content:
                trans.append(tran)
        return [self.header, trans]
    #}}}

    def export_csv (self, fn: str, enc: str):
        """Export financial table"""    #{{{
        with open(fn, 'w', encoding = enc) as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.table[0])
            f_csv.writerows(self.table[1])
    #}}}

class GnuCashCSV (FinCSV):
    """Financial CSV manager for GnuCash"""
    def __init__ (self, table = None):
    #{{{
        header_ref = ['Date', 'Transaction ID', 'Number', 'Description', 
                      'Notes', 'Commodity/Currency', 'Void Reason', 'Action', 
                      'Memo', 'Full Account Name', 'Account Name', 
                      'Amount With Sym', 'Amount Num.', 'Reconcile', 
                      'Reconcile Date', 'Rate/Price']
        FinCSV.__init__(self, table, header_ref)
    #}}}

    def search_trans (self, index: int, content: str) -> list:
        """Dummy function"""  #{{{
        print('[Warning] No support!!!')
    #}}}

    def del_trans (self, index: int, content: str) -> list:
        """Dummy function"""  #{{{
        print('[Warning] No support!!!')
    #}}}

    def add_rev_exp_bc (self, ln_no: int, src_trans: list) -> int:  
        """Add a revenue or expenditure from Bluecoins CSV"""   #{{{
        regex      = re.compile(r'\[\{.*\}\]')
        tran_dst   = []
        tran_src   = src_trans[ln_no]
        tran_split = regex.search(tran_src[10])

        tran_dst += [tran_src[1].split(' ')[0]] # [Date]
        tran_dst += ['', '', tran_src[2]]       # [Transaction ID, Number, Description]

        if tran_split:  # [Note]
            note = tran_split.group()
            tran_dst += [note[2:len(note)-2]]
        else:
            note = ''
            tran_dst += [tran_src[10]]

        tran_dst += ['CURRENCY::' + tran_src[4]]    # [Currency]
        tran_dst += ['', '', '', tran_src[9]]       # [Void, Action, Memo, Account]
        tran_dst += ['', '']                        # [Account name, Amount with sym]

        if tran_split:  # [Amount]
            tran_dst += ['']
        elif tran_src[0] == 'Expense':
            tran_dst += [str(float(tran_src[3]) * -1)]
        else:
            tran_dst += [tran_src[3]]

        tran_dst += ['n', '', tran_src[5]]  # [Reconcile, Reconcile date, Rate]

        gc_idx = len(self.trans)
        self.trans.append(tran_dst)

        amounts = 0.0
        while True:
            tran_dst = []
            tran_src = src_trans[ln_no]

            for i in range(0, 8):
                tran_dst += ['']

            if tran_split:  # [Memo]
                tran_dst += [tran_src[10][len(note):]]
            else:
                tran_dst += ['']

            tran_dst += [tran_src[6] + ':' + tran_src[7]]   # [Account]
            tran_dst += ['', '']                            # [Account name, Amount with sym]

            amount = float(tran_src[3])
            if tran_src[0] == 'Expense':
                amount = amount * -1
            amounts = amounts + amount

            tran_dst += [str(amount * -1), 'n']     # [Amount, Reconcile]
            tran_dst += ['', tran_src[5]]           # [Reconcile date, Rate]

            self.trans.append(tran_dst)

            ln_no = ln_no + 1
            if tran_split == None:
                break
            elif (len(src_trans) == ln_no):
                break
            else:
                next_split = regex.search(src_trans[ln_no][10])
                if next_split == None:
                    break
                elif (note != next_split.group()):
                    break

        if tran_split:
            self.trans[gc_idx][12] = str(amounts)

        return ln_no
    #}}}

    def add_tranf_bc (self, ln_no: int, src_trans: list):
        """Add a transfer to table """  #{{{
        tran_dst = []
        tran_src = src_trans[ln_no]
        tran_dst += [tran_src[1].split(' ')[0]]            # [Date]
        tran_dst += ['', '', tran_src[2], tran_src[10]]    # [ID, Number, Description, Note]
        tran_dst += ['CURRENCY::' + tran_src[4]]           # [Currency]
        tran_dst += ['', '', '', tran_src[9]]              # [Void, Action Memo, Full account name]
        tran_dst += ['', '', str(float(tran_src[3]) * -1)] # [Account name, Amount with sym, Amount]
        tran_dst += ['n', '', tran_src[5]]                 # [Reconcile, Reconcile date, Rate]

        self.trans.append(tran_dst)

        ln_no    = ln_no + 1
        tran_dst = []
        tran_src = src_trans[ln_no]

        for i in range(0, 9):
            tran_dst += ['']

        tran_dst += [tran_src[9], '', '']               # [Full account name, account, amount with sym]
        tran_dst += [tran_src[3], 'n', '', tran_src[5]] # [Amount, Reconcile, Reconcile date, Rate]

        self.trans.append(tran_dst)

        return ln_no + 1
    #}}}

    def import_bc_trans1 (self, fn: str):
        """Read Bluecoins CSV and convert to GnuCash CSV""" #{{{
        src_trans = self.get_trans(fn, 'UTF-8', 1)
        ln_no = 0
        while ln_no < len(src_trans):
            if src_trans[ln_no][0] == 'Transfer':
                ln_no = self.add_tranf_bc(ln_no, src_trans)
            else:
                ln_no = self.add_rev_exp_bc(ln_no, src_trans)
    #}}}

    def import_bc_trans2 (self, src_trans: list):
        """Read Bluecoins CSV and convert to GnuCash CSV""" #{{{
        ln_no = 0
        while ln_no < len(src_trans):
            if src_trans[ln_no][0] == 'Transfer':
                ln_no = self.add_tranf_bc(ln_no, src_trans)
            else:
                ln_no = self.add_rev_exp_bc(ln_no, src_trans)
    #}}}

class BluecoinsCSV (FinCSV):
    """Financial CSV manager for Bluecoins"""
    def __init__ (self, table = None):
    #{{{
        header_ref = ['Type', 'Date', 'Item', 'Amount', 'Currency', 
                      'ConversionRate', 'Parent Category', 'Category', 
                      'Account Type', 'Account', 'Notes', 'Label', 'Status', 
                      'Split']
        FinCSV.__init__(self, table, header_ref)
    #}}}

    def add_rev_exp_am (self, ln_no: int, src_trans: list) -> int:
        """Add a revenue or expenditure to table """    #{{{
        tran_dst = []
        tran_src = src_trans[ln_no]

        tran_dst += ['Expense']     # [Type]

        date = tran_src[5]
        date =  date[4:6] + '/' + date[6:8] + '/' + date[0:4]

        time = tran_src[13]
        for i in range(len(time), 4):
            time = '0' + time
        time = time[0:2] + ':' + time[2:4]

        tran_dst += [date + ' ' + time]  # [Date]
        tran_dst += [tran_src[11]]       # [Item]
        tran_dst += [tran_src[2]]        # [Amount]
        tran_dst += ['TWD', '1']         # [Currency, ConversionRate]
        tran_dst += tran_src[3:5]        # [Parent Category, Category]
        tran_dst += ['', tran_src[6]]    # [Account type, Account]

        note = ""
        for line in tran_src[8].split(' \\n '):
            note = note + line + '\n'

        tran_dst += [note[:len(note)-1]]  # [Note]
        tran_dst += ['', '', '']          # [Label, Status, Split]

        self.trans.append(tran_dst)

        return ln_no + 1
    #}}}

    def import_am_trans (self, fn: str):
        """Import AndroMoney CSV and convert to Bluecoins CSV"""    #{{{
        src_trans = self.get_trans(fn, 'Big5', 2)
        ln_no = 0
        while ln_no < len(src_trans):
            ln_no = self.add_rev_exp_am(ln_no, src_trans)
    #}}}

    def import_bc_trans (self, fn: str):
        """Import Bluecoins CSV from App"""     #{{{
        regex     = re.compile(r'\[\{.*\}\]')
        src_trans = self.get_trans(fn, 'UTF-8', 1)

        for tran_src in src_trans:
            tran_dst = []
            if tran_src[0] == '轉帳':           # [Type]
                tran_dst.append('Transfer')
            elif float(tran_src[4]) < 0.0:
                tran_dst.append('Expense')
            else:
                tran_dst.append('Income')

            date = tran_src[1]
            date = date[5:7] + '/' + date[8:10] + '/' + date[0:4] + ' ' + date[11:16]
            tran_dst += [date, tran_src[3]]       # [Date, Item]
            tran_dst += [abs(float(tran_src[4]))] # [Amount]
            tran_dst += tran_src[5:9]             # [Currency, Rate, Parent Category, Category]
            tran_dst += ['']                      # [Account type]
            tran_dst += tran_src[9:12]            # [Account, Note, Label]
            tran_dst += ['']                      # [Status]

            if regex.search(tran_src[10]):        # [Split]
                tran_dst += ['split']

            self.trans.append(tran_dst)
    #}}}

### Main Function ###

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Financial CSV Convertor\n')
        print('Usage: python FinCSV.py <type> <csv_in> <csv_out>\n')
        print('Argument:\n')
        print('  type       1: Bluecoins (App)      -> GnuCash')
        print('             2: Bluecoins (Templete) -> GnuCash')
        print('             3: AndroMoney           -> Bluecoins')
        print('  csv_in     input CSV file name')
        print('  csv_out    output CSV file name\n')
    elif sys.argv[1] == '1':
        bc_csv = BluecoinsCSV()
        bc_csv.import_bc_trans(sys.argv[2])
        gc_csv = GnuCashCSV()
        gc_csv.import_bc_trans2(bc_csv.trans)
        gc_csv.export_csv(sys.argv[3], 'UTF-8')
    elif sys.argv[1] == '2':
        gc_csv = GnuCashCSV()
        gc_csv.import_bc_trans1(sys.argv[2])
        gc_csv.export_csv(sys.argv[3], 'UTF-8')
    elif sys.argv[1] == '3':
        bc_csv = BluecoinsCSV()
        bc_csv.import_am_trans(sys.argv[2])
        bc_csv.export_csv(sys.argv[3], 'UTF-8')
    else:
        print('Error type!!!')



# -*- coding: utf-8 -*-
# SSW 555 - WS
# Homework 06 - Smelly Codes
# wenkai xiao
# cwid 10471308

import sys, os
from typing import List, Dict, Optional, IO
from prettytable import PrettyTable
from datetime import datetime

def program_header(msg: str) -> None:

    print('\n' + msg)
    print('*' * (len(msg)) + '\n')

def quit() -> None:

    print("\n* Thanks You! *\n")
    sys.exit()

# func, read input file
def get_file(file_name: str) -> IO:

    curr_script_path = os.path.split(os.path.realpath(__file__))[0] + '/'

    while True:

        try:
            get_FileName: str = curr_script_path + file_name
            gotten_File: IO = open(get_FileName, 'r', encoding = 'gbk', errors = 'ignore')
            return gotten_File 

        except FileNotFoundError:
            print("The file does not exist or invalid file name.\n")
            sys.exit()

class File_Analyzer:
    """ Analyze and summarize the GEDCOM file and then output as the needed format. """

    def __init__(self, open_file_command: IO) -> Optional[List]:
     
        self.open_file_command = open_file_command

        self.label_keys: List = ['ID', 'Birthday', 'Passdate', 'Name', 'Gender']
        
        self.get_individuals_with_brithNdeath_info()        
        self.format_individuals_with_brithNdeath_info()

        self.pretty_print()

    """ BAD SMELLS - NEED REFACTORING BELOW """
    # ((method)) 01 <- !!! This method has two bad smells. !!!
    def get_individuals_with_brithNdeath_info(self) -> Optional[List]:
        # ! The 1st Bad Smell !
        """ !!! The first of this method's bad smells reason is that the naming for the variables is too simple,
        which causes the hard undersatndability. """
        # ! The 2nd Bad Smell !
        """ !!! The second of this method's bad smells reason is that it unnecssarily contains the gedcom file reading,
        which causes the hard maintainability. """

        # ! This coding block is the 2nd bad smell due to using the direct file openning approach,
        # making the codes maintaining hard ! #
        file = open(self.open_file_command)
        
        wrap_free_lines: List = []
        line: str
        for line in file:
            line = line.strip('\n')
            wrap_free_lines.append(line)
            # ! Block ends ! #
        
        # ! This coding block is the 1st bad smell due to setting the variables too simple,
        # making the codes reading and understanding hard ! #
        ihx: int
        itx: int
        cx: int = 0
        for line in wrap_free_lines:
            cx += 1
            if line == '0 @I1@ INDI':
                ihx = cx
            elif line == '0 @F1@ FAM':
                itx = cx
        
        i_block: List = wrap_free_lines[ihx - 1 : itx - 1]
        i_block = i_block + ['0 End of INDI 0']

        each_individ_com: List = []
        ucx: int = 0
        uhx: int = 0
        each_individ: List = []
        for unit in i_block[uhx : ]:                
            ucx += 1
            if ('0' and 'INDI' in unit) and (unit != i_block[uhx]):
                each_individ = i_block[uhx : ucx - 1]                    
                uhx = ucx - 1                
                each_individ_com.append(each_individ)

        d_individ_with_bd_com: List = []
        for individ in each_individ_com:
            if 'BIRT' in individ[6]:
                if 'DEAT' in individ[8]:
                    d_individ_with_bd_com.append(individ)

        return d_individ_with_bd_com        
    """ BAD SMELLS END """

    def format_individuals_with_brithNdeath_info(self) -> Optional[List]:

        birth_before_death_info_rows: List = []

        cur_ID: int = 0
        for dead_individual in self.get_individuals_with_brithNdeath_info():
            formatted_row: Dict = dict.fromkeys(self.label_keys)

            cur_ID += 1
            if cur_ID <= 9:
                formatted_row['ID'] = 'I' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                formatted_row['ID'] = 'I' + str(cur_ID)

            for item in dead_individual:

                if 'BIRT' in item:
                    b_date: datetime = datetime.strptime(dead_individual[7][7:], '%d %b %Y')
                    formatted_row['Birthday'] = str(b_date.date())

                if 'DEAT' in item:
                    d_date: datetime = datetime.strptime(dead_individual[9][7:], '%d %b %Y')
                    formatted_row['Passdate'] = str(d_date.date())

                if 'NAME' in item:
                    formatted_row['Name'] = item[7:]

                if 'SEX' in item:
                    formatted_row['Gender'] = item[6:]

            birth_before_death_info_rows.append(formatted_row)

        return birth_before_death_info_rows

    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """
                  
        birth_before_death_table: PrettyTable = PrettyTable(self.label_keys)
        i: Dict
        for i in self.format_individuals_with_brithNdeath_info():
            birth_before_death_table.add_row([v for k, v in i.items()])
        
        print('Birth Before Death:')
        print(birth_before_death_table)

def main():

    File_Analyzer( get_file('WXF.ged') )
    quit()

if __name__ == '__main__':
    main()

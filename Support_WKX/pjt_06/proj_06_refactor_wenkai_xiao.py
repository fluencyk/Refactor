# -*- coding: utf-8 -*-
# SSW 555 - WS
# Homework 06 - Refactor Codes
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

    def __init__(self, open_file_command: IO) -> Optional[List]:
     
        self.open_file_command = open_file_command

        self.label_keys: List = ['ID', 'Birthday', 'Passdate', 'Name', 'Gender']

        self.lines = self.get_gedcom_file_lines()
        
        self.get_individuals_with_brithNdeath_info()        
        self.format_individuals_with_brithNdeath_info()

        self.pretty_print()

    """ REFACTORING BELOW """
    # ((method)) 0.5 <- ! This method is the gedcom file reading functionality that has been extracted from below method !
    def get_gedcom_file_lines(self) -> Optional[List]:
        """ A newly encapsulated method with a succint functionality of reading a gedcom file then returning a list needed """

        with self.open_file_command:

            wrap_free_lines: List = []
            line: str
            for line in self.open_file_command.readlines():
                line = line.strip('\n')
                wrap_free_lines.append(line)

        return wrap_free_lines

    """ REFACTORING BELOW """
    # ((method)) 01 <- ! This method has been done of refactoring !
    def get_individuals_with_brithNdeath_info(self) -> Optional[List]:
        """ For the bad smell 1, this method has been improved by extracting the distracting functionality of reading gedcom file. """
        """ For the bad smell 2, this method has been improved by changing the hard undertandable naming of the variables. """

        # ! This coding block is the 2nd bad smell due to using the direct file openning approach,
        # making the codes maintaining hard ! #
        # file = open(self.open_file_command)
        
        # wrap_free_lines: List = []
        # line: str
        # for line in file:
            # line = line.strip('\n')
            # wrap_free_lines.append(line)
            # ! Block ends ! #

        individuals_head_index: int
        individuals_tail_index: int
        cur_index: int = 0
        for line in self.lines:
            cur_index += 1
            if line == '0 @I1@ INDI':
                individuals_head_index = cur_index
            elif line == '0 @F1@ FAM':
                individuals_tail_index = cur_index
        
        individuals_block: List = self.lines[individuals_head_index - 1 : individuals_tail_index - 1]
        individuals_block = individuals_block + ['0 End of INDI 0']

        each_individual_combination: List = []
        unit_cur_index: int = 0
        unit_head_index: int = 0
        each_individual: List = []
        for unit in individuals_block[unit_head_index : ]:                
            unit_cur_index += 1
            if ('0' and 'INDI' in unit) and (unit != individuals_block[unit_head_index]):
                each_individual = individuals_block[unit_head_index : unit_cur_index - 1]                    
                unit_head_index = unit_cur_index - 1                
                each_individual_combination.append(each_individual)

        dead_individual_with_birth_and_death_combination: List = []
        for individual in each_individual_combination:
            if 'BIRT' in individual[6]:
                if 'DEAT' in individual[8]:
                    dead_individual_with_birth_and_death_combination.append(individual)

        return dead_individual_with_birth_and_death_combination

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

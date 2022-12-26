# -*- coding: utf-8 -*-
# SSW 555 - WS
# Homework 04
# wenkai xiao
# cwid 10471308

import sys, os
from typing import List, Optional, IO, Dict
from datetime import datetime
from prettytable import PrettyTable

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
        self.individuals_table_labels: List = ['ID', 'Name', 'Birthday']
        self.families_table_labels: List = ['ID', 'Husband', 'Wife']

        self.lines = self.get_gedcom_file_lines()
        self.individuals_and_families = self.get_individuals_and_families()

        self.individuals_with_name_and_birthday = self.format_individuals_with_name_and_birthday()
        self.families_by_spouses = self.format_families_by_spouses()

        self.pretty_print() 

    def get_gedcom_file_lines(self) -> Optional[List]:

        with self.open_file_command:

            wrap_free_lines: List = []
            line: str
            for line in self.open_file_command.readlines():
                line = line.strip('\n')
                wrap_free_lines.append(line)

        return wrap_free_lines
   
    def get_individuals_and_families(self) -> Optional[List]:

        individuals_head_index: int
        individuals_tail_index: int
        families_head_index: int
        families_tail_index: int
        cur_index: int = 0
        for line in self.lines:
            cur_index += 1
            if line == '0 @I1@ INDI':
                individuals_head_index = cur_index
            elif line == '0 @F1@ FAM':
                individuals_tail_index = cur_index
                families_head_index = cur_index
            elif line == '0 TRLR':
                families_tail_index = cur_index
        
        individuals_block: List = self.lines[individuals_head_index - 1 : individuals_tail_index - 1]
        individuals_block = individuals_block + ['0 End of INDI 0']
        families_block: List = self.lines[families_head_index - 1 : families_tail_index -1]
        families_block = families_block + ['0 End of FAM 0']
        
        unit_cur_index: int = 0
        unit_head_index: int = 0
        each_individual_combination: List = []
        each_individual: List = []
        for unit in individuals_block[unit_head_index : ]:                
            unit_cur_index += 1
            if ('0' and 'INDI' in unit) and (unit != individuals_block[unit_head_index]):
                each_individual = individuals_block[unit_head_index : unit_cur_index - 1]                    
                unit_head_index = unit_cur_index - 1                
                each_individual_combination.append(each_individual)

        elem_cur_index: int = 0
        elem_head_index: int = 0
        each_family_combination: List = []
        each_family: List = []
        for elem in families_block[elem_head_index : ]:
            elem_cur_index += 1
            if ('0' and 'FAM' in elem) and (elem != families_block[elem_head_index]):
                each_family = families_block[elem_head_index : elem_cur_index - 1]
                elem_head_index = elem_cur_index - 1
                each_family_combination.append(each_family)

        individuals_and_families: List = []
        individuals_and_families.append(each_individual_combination)
        individuals_and_families.append(each_family_combination)

        #print(individuals_and_families[0])
        return individuals_and_families
   
    def format_individuals_with_name_and_birthday(self) -> Optional[List]:

        name_and_birthday_rows: List = []

        cur_ID: int = 0
        for unique_individual in self.individuals_and_families[0]:
            formatted_row: Dict = dict.fromkeys(self.individuals_table_labels)

            cur_ID += 1
            if cur_ID <= 9:
                formatted_row['ID'] = 'I' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                formatted_row['ID'] = 'I' + str(cur_ID)

            item: str
            cur_index: int = 0
            for item in unique_individual:                
                cur_index += 1

                if 'NAME' in item:
                    item = [i for i in item.split(' ')]
                    formatted_row['Name'] = ' '.join(item[2:])

                if 'BIRT' in item:
                    birth_item = [i for i in str(unique_individual[cur_index]).split(' ')]
                    if len(birth_item) == 5:
                        b_date: datetime = datetime.strptime(' '.join(birth_item[2:]), '%d %b %Y')
                        formatted_row['Birthday'] = str(b_date.date())

            if formatted_row['Birthday'] == None:
                continue
            name_and_birthday_rows.append(formatted_row)

        return name_and_birthday_rows

    def format_families_by_spouses(self) -> Optional[List]:

        families_by_spouses: List = []

        cur_ID: int = 0

        for unique_family in self.individuals_and_families[1]:
            formatted_row: Dict = dict.fromkeys(self.families_table_labels)

            cur_ID += 1
            if cur_ID <= 9:
                formatted_row['ID'] = 'I' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                formatted_row['ID'] = 'I' + str(cur_ID)

            item: str
            for item in unique_family:
                cur_item = [i for i in item.split(' ')]

                if cur_item[1] == 'HUSB':
                    for individual in self.individuals_and_families[0]:
                        for elem in individual:
                            elem = elem.split(' ')
                            if cur_item[2].strip('@') == elem[1].strip('@'):
                                formatted_row['Husband'] = individual[1][7:]

                if cur_item[1] == 'WIFE':
                    for individual in self.individuals_and_families[0]:
                        for elem in individual:
                            elem = elem.split(' ')
                            if cur_item[2].strip('@') == elem[1].strip('@'):
                                formatted_row['Wife'] = individual[1][7:]

            families_by_spouses.append(formatted_row)

        return families_by_spouses

    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """
                  
        name_and_birthday: PrettyTable = PrettyTable(self.individuals_table_labels)
        i: Dict
        for i in self.individuals_with_name_and_birthday:
            name_and_birthday.add_row([v for k, v in i.items()])
        
        print('Unique Name and Birth Date: < User Story No.23 >')
        print(name_and_birthday)

        families_by_spouses: PrettyTable = PrettyTable(self.families_table_labels)
        i: Dict
        for i in self.families_by_spouses:
            families_by_spouses.add_row([v for k, v in i.items()])
        
        print('Families by Spouses: < User Story No.24 >')
        print(families_by_spouses)

def main():

    program_header('User Story 23, 24')
    File_Analyzer( get_file('WXF.ged') )
    quit()

if __name__ == '__main__':
    main()

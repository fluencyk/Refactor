# ===== Python - UTF-8 ===== #
"""/*
School: Stevens Institute of Technology
---------------------------------------
Course: SSW 555 - WS
Instructor: Prof. Richard Ens
--------------------------------------
Project: # 06 / User Stories: 021, 022
--------------------------------------
Coder with CWID: Yujun Kong / 1046 6820
Team with members # 04: Kristin Allocco / Shengping Xu / Yujun Kong
*/"""
# ===== CODING BEGINS ===== #

# * import the supporting types, libraries, modules
from multiprocessing.dummy.connection import families
import sys
from typing import Any, List, Set, Dict, Optional, IO
from prettytable import PrettyTable
from datetime import datetime

""" # Global Objects Begin # """
# {format} for to print blank line:
def BL():
    print ()

# {format} for to print a separating line:
def SL():
    print ('-' * 150)

# {format} for to print if some codes are okay:
def OK():
    print ('Okay')
# {/}
""" # /Global Objects End # """

""" # Supporting Classes Begin # """
# <class> define supporting class"ezIO" for to reuse codes:
class ezIO:

    # ([constructor]) define a constructor for class itself:
    def __init__(self):
        pass #! Temporarily, there're no needs.
    
    # ((method)) define a method for to print out the welcoming words:
    def welcome(self):

        welcoming = "-== Welcome to ' User Stories: 021, 022 ' ==-"
        BL()
        print(welcoming)
        print ( '-' * len(welcoming) )
        BL()
    # ((/))

    # ((method)) define a method for to quit the main program:
    def quit_Main(self):

        BL()
        print("--- Thanks for your operating, Bye! ---")
        BL()
        sys.exit()
    # ((/))

    # ((method))
    def open_file(self, file_name: str) -> IO:

        while True:
            try:
                gotten_File: IO = open(file_name, 'r', encoding = 'gbk', errors = 'ignore')
                return gotten_File
            except FileNotFoundError:
                print("The file name is invalid or the file does not exist, program ends!")
                sys.exit()
                BL()
                continue
    # ((/))
# </>
""" # /Supporting Classes End # """


""" # CORE DEFINING BEGINS HERE # """
# --------------------------------- #

""" # 01 Unit """
# <class>
class File_Analyzer:
    """ Analyze and summarize the GEDCOM file and then output as the needed format. """

    # ((method)) Constructor
    def __init__(self, open_file_command: IO) -> Optional[List]:
     
        self.open_file_command = open_file_command
        self.individuals_table_labels: List = ['ID', 'Name', 'Birthday']
        self.families_table_labels: List = ['ID', 'Husband', 'Wife']
        self.validation_table_labels: List = ['ID', 'Name', 'Family Role', 'Gender Validation']

        self.lines = self.get_gedcom_file_lines()
        self.individuals_and_families = self.get_individuals_and_families()

        self.individuals_with_name_and_birthday = self.format_individuals_with_name_and_birthday()
        self.families_by_spouses = self.format_families_by_spouses()
        self.role_gender_validation = self.validate_gender_for_role()
        self.id_uniqueness_validation = self.validate_uniqueness_for_id()

        self.pretty_print()        
    # ((/))

    # ((method)) 0.5
    def get_gedcom_file_lines(self) -> Optional[List]:

        with self.open_file_command:

            wrap_free_lines: List = []
            line: str
            for line in self.open_file_command.readlines():
                line = line.strip('\n')
                wrap_free_lines.append(line)

        return wrap_free_lines
    # ((/))

    # ((method)) 01
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
    # ((/))

    # ((method)) 02 <- User Story #23
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
    # ((/))

    # ((method)) 03 <- User Story #24
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
    # ((/))

    # ((method)) 04 <- User Story #21
    def validate_gender_for_role(self) -> Optional[List]:

        gender: str
        gender_validation: List = []
        role_and_id: List = []
        role_and_gender: List = []
        item: str
        elem: str
        unit: str

        for each_family in self.individuals_and_families[1]:
            for elem in each_family:
                cur_elem = [i for i in elem.split(' ')]
                if 'HUSB' in cur_elem:
                    role_and_id.append([cur_elem[1]] + [cur_elem[2]])
                elif 'WIFE' in cur_elem:                    
                    role_and_id.append([cur_elem[1]] + [cur_elem[2]])

        for each_person in self.individuals_and_families[0]:
            person: List = []
            for item in each_person:
                cur_item = [i for i in item.split(' ')]
                if 'INDI' in cur_item:
                    person.append(cur_item[1])
                if 'NAME' in cur_item:
                    person.append(cur_item[2] + ' ' + cur_item[3].strip('/'))
                if 'SEX' in cur_item:
                    person.append(cur_item[2])
            role_and_gender.append(person)

        each_role: str
        for each_role in role_and_id:
            formatted_row: Dict = dict.fromkeys(self.validation_table_labels)

            formatted_row['ID'] = each_role[1].strip('@')

            if each_role[0] == 'HUSB':
                formatted_row['Family Role'] = 'Husband'
                gender = 'M'
                for each_one in role_and_gender:
                    if each_role[1] == each_one[0]:
                        formatted_row['Name'] = each_one[1]
                        if each_one[2] == gender:
                            formatted_row['Gender Validation'] = 'Correct'
                        if each_one[2] != gender:
                            formatted_row['Gender Validation'] = 'Wrong!'

            if each_role[0] == 'WIFE':
                formatted_row['Family Role'] = 'Wife'
                gender = 'F'
                for each_one in role_and_gender:
                    if each_role[1] == each_one[0]:
                        formatted_row['Name'] = each_one[1]
                        if each_one[2] == gender:
                            formatted_row['Gender Validation'] = 'Correct'
                        if each_one[2] != gender:
                            formatted_row['Gender Validation'] = 'Wrong!'            

            gender_validation.append(formatted_row)

        return gender_validation
    # ((/))

    # ((method)) 05 <- User Story #22
    def validate_uniqueness_for_id(self) -> Optional[bool]:

        all_individual_ids: List = []
        individual_ids_set: Set = ()

        all_family_ids: List = []
        family_ids_set: Set = ()

        atom: str
        for each_individual in self.individuals_and_families[0]:
            for atom in each_individual:
                cur_atom = [i for i in atom.split(' ')]
                if 'INDI' in atom:
                    all_individual_ids.append(cur_atom[1].strip('@'))

        item: str
        for each_family in self.individuals_and_families[1]:
            for item in each_family:
                cur_item = [i for i in item.split(' ')]
                if 'FAM' in item:
                    all_family_ids.append(cur_item[1].strip('@'))

        individual_ids_set = set(all_individual_ids)
        family_ids_set = set(all_family_ids)

        if len(individual_ids_set) + len(family_ids_set) == len(all_individual_ids) + len(all_family_ids):
            return True
        else:
            return False
    # ((/))

    # ((method)) 0E_02
    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """
                  
        name_and_birthday: PrettyTable = PrettyTable(self.individuals_table_labels)
        i: Dict
        for i in self.individuals_with_name_and_birthday:
            name_and_birthday.add_row([v for k, v in i.items()])
        
        #print('Unique Name and Birth Date: < User Story No.23 >')
        #print(name_and_birthday)
        #BL()

        families_by_spouses: PrettyTable = PrettyTable(self.families_table_labels)
        i: Dict
        for i in self.families_by_spouses:
            families_by_spouses.add_row([v for k, v in i.items()])
        
        #print('Families by Spouses: < User Story No.24 >')
        #print(families_by_spouses)
        #BL()

        role_gender_validation_outcomes: PrettyTable = PrettyTable(self.validation_table_labels)
        i: Dict
        for i in self.role_gender_validation:
            role_gender_validation_outcomes.add_row([v for k, v in i.items()])

        print('Family Roles Gender Validation: < User Story No.21 >')
        print(role_gender_validation_outcomes)
        BL()

        print('Family Roles Gender Validation: < User Story No.22 >')
        if self.id_uniqueness_validation == False:
            print('-=== Individual and Family IDs are Not Unique! ===-')
            BL()
        elif self.id_uniqueness_validation == True:
            print('-=== Individual and Family ID are Fully Unique. ===-')
            BL()
    # ((/))

# </>

# ------------------------------- #
""" # CORE DEFINING ENDS HERE # """


"""///*** define main program and execute it below ***///"""

# (((main function)))
def main(): #!! <- Main Program Procedure Flow !!#

    e = ezIO() #! <- Supporting Input/Output Class !#

    e.welcome() #! <- Print Out The Header !#
    
    File_Analyzer( e.open_file('YKF.ged') )
    SL()
    BL()
    
    # // "quit the program"
    e.quit_Main()
# (((/main function)))

"""///*** main program execute below ***///"""

if __name__ == '__main__':
    main()

"""///*** main program define and execution ends ***///"""

# ===== CODING ENDS ===== #
# //


# /// The Coding Experience and Conclusion ///
"""/'

Nope...

'/"""
# ///
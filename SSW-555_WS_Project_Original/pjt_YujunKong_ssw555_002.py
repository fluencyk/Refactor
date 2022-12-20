# ===== Python - UTF-8 ===== #
"""/*
School: Stevens Institute of Technology
---------------------------------------
Course: SSW 555 - WS
Instructor: Prof. Richard Ens
---------------------------------------------------------
Project: # 02 / Read, Analyze, & Print GEDCOM Format File
---------------------------------------------------------
Coder with CWID: Yujun Kong / 1046 6820
*/"""
# //
# ===== CODING BEGINS ===== #


# * import the potentially needed utilities *
import sys

# * import the supporting types *
from typing import Any, List, Optional, IO, Tuple


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

# {//}
""" # /Global Objects End # """


""" # Supporting Classes Begin # """
# <class> define supporting class"ezIO" for to reuse codes:
class ezIO:

    # ([constructor]) define a constructor for class itself:
    def __init__(self):
        pass #! Temporarily, there're no needs.
    
    # ((method)) define a method for to print out the welcoming words:
    def welcome(self):

        welcoming = "-== Welcome to ' Read, Analyze, & Print GEDCOM Format File ' ==-"
        BL()
        print(welcoming)
        print ( '-' * len(welcoming) )
        BL()

    # ((method)) define a method for to quit the main program:
    def quit_Main(self):

        BL()
        print("--- Thanks for your operating, Bye! ---")
        BL()
        sys.exit()

    # ((method)) define a method for to get user's string like words sequence:
    def get_String_Like_Input(self, prompt: Any) -> Optional[str]:
        pass #! Temporarily, there're no needs.

    # ((/))
# </>
""" # /Supporting Classes End # """


""" # CORE DEFINING BEGINS HERE # """
# --------------------------------- #

""" # 01 function """
# (function) define a function for to open a file and get the file with the following operations:
def get_File() -> IO:
    """ Open a file to operate if the file exist, or print out the exception. """

    e = ezIO() #! <- For to use the supporting class.

    while True:

        try:
            get_FileName: str = "YKF.ged"
            gotten_File: IO = open(get_FileName, 'r', encoding = 'gbk', errors = 'ignore')
            return gotten_File 

        except FileNotFoundError:
            print("The file name is invalid or the file does not exist.")
            BL()
            continue
        
# (/function)

""" # 02 function """
# (function) define a function for to open a file and get the file with the following operations:
def read_and_print_gedcom_file(theFile: IO) -> Optional[List]:
    """ Operate the openned GEDCOM format file to read, analyze, and print lines. """

    supported_Tags_Set: Tuple = ('INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
                                 'FAMC', 'FAMS', 'FAM',
                                 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV',
                                 'DATE', 'HEAD', 'TRLR', 'NOTE') #! <- The GEDCOM format supported tags set.

    __Valid_Tag_Stamp: str = 'Y'
    __Invalid_Tag_Stamp: str = 'N'
    
    with theFile:

        line: str
        for line in theFile.readlines():
            print(f"--> {line}", end='')

            line = line.strip('\n') 
            splitted_Line: List = [ tag for tag in line.split(' ') ]
            validated_Line: List = []

            for tag in splitted_Line:
                validated_Line.append(tag)
            if splitted_Line[1] in supported_Tags_Set:
                validated_Line.insert(2, __Valid_Tag_Stamp)
            elif splitted_Line[1] not in supported_Tags_Set:
                validated_Line.insert(2, __Invalid_Tag_Stamp)

            print(f"<-- {'|'.join(validated_Line)}", end='')
            print('\n', end="")
      
# (/)

# ------------------------------- #
""" # CORE DEFINING ENDS HERE # """


"""///*** define main program and execute it below ***///"""
# (((main function)))
def main(): #!! <- Main Program Procedures !!#

    e = ezIO() #! <- For to use the supporting class.

    e.welcome()
    
    read_and_print_gedcom_file( get_File() )
        
    e.quit_Main()

# (((/)))

"""///*** main program execute below ***///"""

if __name__ == '__main__':
    main()

"""///*** main program define and execution ends ***///"""

# ===== CODING ENDS ===== #
# //



# /// The Coding Experience and Conclusion ///
"""/'

Nope, thanks!

'/"""
# ///
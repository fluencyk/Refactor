# -*- coding: utf-8 -*-
# SSW 555 - WS
# Homework 04 - Test Case
# wenkai xiao
# cwid 10471308

import sys, unittest
from typing import Optional, List, Tuple, DefaultDict, Set
from proj_04_wenkai_xiao import File_Analyzer

class File_Analyzer_Test_Cases(unittest.TestCase):

    def test_file_analyzer_01(self):
        
        fa = File_Analyzer
        self.assertIsNotNone(fa.format_families_by_spouses, 'Is Not None')

    def test_file_analyzer_02(self):

        self.assertNotEqual(File_Analyzer.get_individuals_and_families, File_Analyzer.format_individuals_with_name_and_birthday)

    def test_file_analyzer_03(self):

        fa = File_Analyzer
        self.assertIs(fa.get_gedcom_file_lines, File_Analyzer.get_gedcom_file_lines)

    def test_file_analyzer_04(self):

        fa = File_Analyzer
        self.assertIsNot(fa.get_individuals_and_families, File_Analyzer.get_gedcom_file_lines)

    def test_file_analyzer_05(self):

        fa = File_Analyzer
        self.assertNotIsInstance(fa, File_Analyzer, 'Is a Instance')

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)

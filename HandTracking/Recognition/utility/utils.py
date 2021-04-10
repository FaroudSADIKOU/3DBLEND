"""
"""

# %% Imports
import pandas as pd
import numpy as np

import os, sys, inspect
import glob
from .real_parser import Parser

# %%
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
dataset_dir = os.path.abspath(os.path.join(src_dir, '../dataset/'))

# %%
class Utils():
    def __init__(self):
        self.parser = Parser()

    def __get_all_file_names(self) -> list:
        """
        """
        # build the path name pattern
        pathname_pattern = os.path.abspath(os.path.join(dataset_dir, "**/*.csv"))
        return glob.glob(pathname_pattern, recursive=True)

    def load_data(self):
        # get the list of all the skeleteal data file name.
        all_data_filename = self.__get_all_file_names()
        # for each get the content as a dataframe
        list_of_dada = list(map(lambda a_file_name: self.parser.parse(a_file_name), all_data_filename))
        # fuze all together in one dataframe
        datas = pd.concat(list_of_dada, ignore_index=True)
        return datas
    
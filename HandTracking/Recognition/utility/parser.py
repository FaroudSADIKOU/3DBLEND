"""

"""
# %% Imports
import pandas as pd
import numpy as np

import os, sys, inspect
import glob

# %%
NB_DATA_FRAME_PER_FILE = 500
NB_VALUE_PER_FRAME = 36
columns_dict = {
    "palm_x": 0, "palm_y": 1, "palm_z": 2, "normal_x": 3, "normal_y": 4, "normal_z": 5,
    "thumb_x": 6, "thumb_y": 7, "thumb_z": 8, "index_x": 9, "index_y": 10, "index_z": 11,
    "middle_x": 12, "middle_y": 13, "middle_z": 14, "ring_x": 15 , "ring_y": 16, "ring_z": 17,
    "pinky_x": 18, "pinky_y": 19, "pinky_z": 20
}
TARGET_COL_NAME = 'target_name'
""" index of data not to keep from the file. Represent the index 
where are located the value of the pointing direction of the each finger.
"""
to_drop_index = (9, 10, 11, 15, 16, 17, 21, 22, 23, 27, 28, 29, 33, 34, 35)

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
dataset_dir = os.path.abspath(os.path.join(src_dir, '../dataset/'))
# %%

class Parser():
    def __init__(self):
        pass
    
    def get_target_from_filename(self, filename: str) -> str:
        target = None
        if(filename):
            target = filename.split(os.path.sep)[-1].split('.')[0]
        return target

    def parse(self, file_name) -> pd.DataFrame:
        """ 
        """
        data = None
        # retrive the target name "alias class"
        targetname = self.get_target_from_filename(file_name)
        try:
            with open(file_name) as a_file:
                matrix = [
                    np.delete(
                        [
                            float(next(a_file)) for cord in range(NB_VALUE_PER_FRAME)
                        ], to_drop_index
                    ) for frame in range(NB_DATA_FRAME_PER_FILE)
                ]
                
                data = pd.DataFrame(matrix, columns=columns_dict.keys())
                data[TARGET_COL_NAME] = targetname
        except FileExistsError as er:
            print(er)
        finally:
            return data

# %%
# # TODO to delete
# def main():
#     # This is just a test case
#     parser = Parser()
#     filename = os.path.abspath(os.path.join(dataset_dir, "PersonA/1.txt"))
#     data = parser.parse(filename)
#     print(data)
# # # %%
# if __name__ == '__main__':
#     main()

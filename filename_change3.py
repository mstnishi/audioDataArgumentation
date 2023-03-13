#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Argumentation
"""
__author__ = "Nishimoto"
__version__ = "1.0.0"
__date__ = "2023-01-10"

import os
import hashlib
import time

def main():
    data_dir = os.path.exists("data")
    if data_dir == False:
        print("dataディレクトリを作成しました")
        os.mkdir("data")
        return

    output_dir = os.path.exists("output/")
    if output_dir == False:
        print("dataディレクトリを作成しました")
        os.mkdir("output")
        return

    data_path = "./output/"

    files = os.listdir(data_path)
    print("ファイル数 : ", str(len(files)))

    for f in files:
        print("ファイル名 : " + f)
        filename_split_list = f.split(".")
        word_idx_test = find_word_index(filename_split_list, "orig_test")
        word_idx_train = find_word_index(filename_split_list, "orig_train")

        if word_idx_test != False:
            del filename_split_list[word_idx_test]
            ele_cnt = len(filename_split_list)
            newfilename = ""

            for i, j in enumerate(filename_split_list):
                if i != ele_cnt - 1:
                    newfilename += j + "."
                else:
                    newfilename += j

        elif word_idx_train != False:
            del filename_split_list[word_idx_train]
            ele_cnt = len(filename_split_list)
            newfilename = ""

            for i, j in enumerate(filename_split_list):
                if i != ele_cnt - 1:
                    newfilename += j + "."
                else:
                    newfilename += j
        else:
            continue

        file_oldname_path = data_path + f
        file_newname_path = data_path + newfilename
        print(file_oldname_path)
        print(file_newname_path)
        os.rename(file_oldname_path, file_newname_path)
    return


def find_word_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default

if __name__ == "__main__":
    main()

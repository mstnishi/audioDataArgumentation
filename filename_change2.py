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

    data_path = "./data/help/"
    output_path = "./output/"

    files = os.listdir(data_path)
    print("ファイル一覧 : ", files)
    print("ファイル数 : ", str(len(files)))

    for f in files:
        print("ファイル名 : " + f)
        filename_split_list = f.split(".")
        word_idx = find_word_index(filename_split_list, "wav")

        if word_idx != False:
            del filename_split_list[word_idx + 1:]
            ele_cnt = len(filename_split_list)
            newfilename = ""
            dat =  str(time.time())
            hash = hashlib.md5(dat.encode()).hexdigest()

            for i, j in enumerate(filename_split_list):
                if i != ele_cnt - 1:
                    if i == 0:
                        newfilename += "help_jpn" + "."
                    else:
                        newfilename += j + "."
                else:
                    newfilename += hash + "." + j
        file_oldname_path = data_path + f
        file_newname_path = output_path + newfilename
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Argumentation
"""
__author__ = "Nishimoto"
__version__ = "1.0.0"
__date__ = "2023-01-10"

import os

def main():
    file = os.path.exists("data")
    if file == False:
        print("dataディレクトリを作成しました")
        os.mkdir("data")
        return

    print("ディレクトリ名を入力して下さい")
    print("※./data以下のディレクトリ名")
    target_dir = input()
    data_path = "./data/" + target_dir + "/"
    files = os.listdir(data_path)
    print("ファイル一覧 : ", files)
    print("ファイル数 : ", str(len(files)))

    for f in files:
        if f != "desktop.ini":
            print("ファイル名 : " + f)
            filename_split_list = f.split(".")
            word_idx = find_word_index(filename_split_list, "wav")

            if word_idx != False:
                del filename_split_list[word_idx + 1:]
                ele_cnt = len(filename_split_list)
                newfilename = ""

                for i, j in enumerate(filename_split_list):
                    if i != ele_cnt - 1:
                        newfilename += j + "."
                    else:
                        newfilename += j

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Argumentation
"""
__author__ = "Nishimoto"
__version__ = "1.0.0"
__date__ = "2023-01-10"

import os
import random
import librosa
import wave
import struct
import math
import numpy as np
import sox
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy import fromstring, int16

def main():
    file = os.path.exists("data")
    if file == False:
        print("dataディレクトリを作成しました")
        print("dataディレクトリ以下にラベル名のディレクトリを生成し、wavファイルを配置して下さい")
        os.mkdir("data")
        return

    img_file = os.path.exists("img")
    if img_file == False:
        print("imgフォルダを作成しました")
        os.mkdir("img")

    output = os.path.exists("output")
    if output == False:
        print("outputフォルダを作成しました")
        os.mkdir("output")

    print("データの水増しを行うディレクトリ名を入力して下さい")
    print("※./data以下のディレクトリ名")
    target_dir = input()
    data_path = "./data/" + target_dir + "/"
    img_save_path = "./img/"
    output_path = "./output/"
    files = os.listdir(data_path)
    print("ファイル一覧 : ", files)
    print("ファイル数 : ", str(len(files)))
    time = 1
    sr = 16000

    for f in files:
        print("ファイル名 : " + f)
        file_path = data_path + f
        # data = load_audio_file(data_path + f)
        data, _ = librosa.load(file_path, sr=sr)
        file_name = f.replace(".wav", "")
        test = reverb(data, sr, 120)
        save_file_name = file_name + ".stretch" + ".wn" + str(1)
        wn_data_path = output_path + save_file_name + ".wav"
        # plot_time_series(data_wn, wn_img_data_path)
        librosa.audio.sf.write(wn_data_path, test, sr)


        # for j in range(1, 11):
        #     # ホワイトノイズ加工
        #     wn = np.random.randn(len(data))
        #     data_wn = data + 0.005*wn
        #     save_file_name = file_name + ".stretch" + ".wn" + str(j)
        #     wn_data_path = output_path + save_file_name + ".wav"
        #     wn_img_data_path = img_save_path + save_file_name + ".png"
        #     # plot_time_series(data_wn, wn_img_data_path)
        #     librosa.audio.sf.write(wn_data_path, data_wn, sr)

        #     # ピッチ加工
        #     data_pitch = pitch_shift(data, sr, random.uniform(-2, 2))
        #     save_file_name = file_name + ".stretch" + ".pitch" + str(j)
        #     pitch_data_path = output_path + save_file_name + ".wav"
        #     pitch_img_data_path = img_save_path + save_file_name + ".png"
        #     # plot_time_series(data_pitch, pitch_img_data_path)
        #     librosa.audio.sf.write(pitch_data_path, data_pitch, sr)
    return


def load_audio_file(file_path):
    """
    音声データ読込み
    """
    input_length = 16000
    y, sr = librosa.load(file_path)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f'sampling rate:  {sr}')
    print(f'duration:       {duration}\n')
    data = librosa.core.load(file_path, sr=16000)[0]
    data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
    return data


def plot_time_series(data, save_file_path):
    """
    波形確認
    """
    fig = plt.figure(figsize=(14, 8))
    plt.title('Raw wave')
    plt.ylabel('Amplitude')
    plt.plot(np.linspace(0, 1, len(data)), data)
    plt.savefig(save_file_path)


def stretch(data, rate=1):
    """
    時間伸縮
    """
    input_length = 16000
    data = librosa.effects.time_stretch(data, rate)
    data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
    return data


def pitch_shift(data, sample_rate, shift):
    """
    ピッチ変更
    +12:1オクターブ上
    -12:1オクターブ下
    +7:完全５度
    +5:完全４度
    """
    ret = librosa.effects.pitch_shift(data, sample_rate, shift, bins_per_octave=12, res_type='kaiser_best')
    return ret


def time_shift(data, shift):
    """
    タイムシフト
    """
    data_roll = np.roll(data, shift)
    return data_roll


def reverb(data, sample_rate, rate):
    """
    残響
    """
    tfm = sox.Transformer()
    tfm.reverb(rate)
    return tfm.build_array(input_array=data, sample_rate_in=sample_rate)


def volume_change(data, vol_size):
    """
    ボリューム変更
    """
    data_vol = data * vol_size
    return data_vol


def normlize(data):
    """
    ノーマライズ（正規化）
    """
    data_norm = librosa.util.normalize(data)
    return data_norm


def get_totlal_time(file_path, time):
    """
    再生時間取得
    """
    wr = wave.open(file_path, 'r')
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    wr.close()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time)
    frames = int(ch * fr * time)
    num_cut = int(integer // time)
    print("Channel : ", ch)
    print("Sample width : ", width)
    print("Frame Rate : ", fr)
    print("Frame num : ", fn)
    print("Params : ", wr.getparams())
    print("Total time : ", total_time ,"sec")
    print("Total time(integer) : ",integer)
    print("Time : ", time)
    print("Frames : ", frames)
    print("Number of cut : ", num_cut)
    return total_time


def write_wav(file_path, time):
    """
    1秒音声データ書込み
    """
    result = False
    wr = wave.open(file_path, 'r')
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    frames = int(ch * fr * time)
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = fromstring(data, dtype=int16)
    print("X : ", X)
    outf = file_path
    start_cut = 0 * frames
    end_cut = 0 * frames + frames
    print("start_cut : ", start_cut)
    print("end_cut : ", end_cut)
    Y = X[start_cut:end_cut]
    outd = struct.pack("h" * len(Y), *Y)

    try:
        print("ファイル書込み")
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
        result = True
    except:
        print("書き込みに失敗しました")
    return result


def file_time_check(file_path, time):
    """
    1秒音声データ生成
    """
    total_time = get_totlal_time(file_path, time)
    cnt = 0
    while True:
        cnt += 1
        print("total_time : %s"%(total_time))
        if total_time == 1:
            print("1秒ファイルの生成に成功しました")
            break
        elif total_time < 1:
            print("1秒以下の音声データに1秒のサイレントオーディオ追加")
            silent_audio= AudioSegment.silent(duration=1000)
            tmp_file = AudioSegment.from_file(file_path)
            processed_data = tmp_file + silent_audio
            processed_data.export(file_path, format='wav')
            total_time = get_totlal_time(file_path, time)
            continue
        elif total_time > 1:
            print("1秒以上の音声データから1秒の音声データへ変換")
            result = write_wav(file_path, time)
            if result:
                print("ファイルの書き込みに成功しました")
                total_time = get_totlal_time(file_path, time)
            continue
        elif cnt >= 2:
            print("エラー")
            break


if __name__ == "__main__":
    main()
# https://watlab-blog.com/2022/03/05/record-fft-wav/
import pyaudio
import soundfile as sf
import numpy as np
from scipy import fftpack
from matplotlib import pyplot as plt
from pathlib import Path
savefolda = Path("out_audio")

if savefolda.exists() == False:
    savefolda.mkdir()

# 録音する関数
def record(savename):

    # 計測条件を設定
    time = 5
    samplerate = 44100
    fs = 1024
    index = 1
    pa = pyaudio.PyAudio()

    # ストリームの開始
    data = []
    dt = 1 / samplerate
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=samplerate,
                     input=True, input_device_index=index, frames_per_buffer=fs)

    # フレームサイズ毎に音声を録音していくループ
    print("stream")
    for i in range(int(((time / dt) / fs))):
        frame = stream.read(fs)
        print(frame)
        data.append(frame)

    # ストリームの終了
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # データをまとめる処理
    data = b"".join(data)

    # データをNumpy配列に変換/時間軸を作成
    data = np.frombuffer(data, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    t = np.arange(0, fs * (i + 1) * (1 / samplerate), 1 / samplerate)
    sf.write(savefolda.joinpath(savename+".wav"), data, samplerate)
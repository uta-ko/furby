from lib import responce_chatGPT
from lib import transform_audio_to_string
from lib import transform_japanese_to_roman
import pyaudio
import numpy as np
import matplotlib.pyplot as plot
import soundfile as sf
from pathlib import Path
import asyncio
# from Pysound_Error_hider import noalsaerr
"""https://niyanmemo.com/335/"""
savefolda = Path("lib")

savename = "rec"
samplerate = 44100
fs = 1024

if savefolda.exists() == False:
    savefolda.mkdir()

def audiostart():
    # with noalsaerr():
    audio = pyaudio.PyAudio() 
    stream = audio.open( format = pyaudio.paInt16,
                         rate = samplerate,
                         channels = 1, 
                         input_device_index = 1,
                        input = True, 
                        frames_per_buffer = fs)
    return audio, stream

def audiostop(audio, stream):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def read_plot_data(stream):
    data = stream.read(1024)
    audiodata = np.frombuffer(data, dtype='int16')
    volume = audiodata.max()
    return data,volume

(audio,stream) = audiostart()
rec_data = []
cnt =0
silent_cnt = 0
voise_in = False


while True:
    try:
        data,volume = read_plot_data(stream)
        rec_data.append(data)

        if volume < 200:
            silent_cnt += 1
        else:
            voise_in = True
            silent_cnt = 0

        if silent_cnt > 30 and voise_in:
            if len(rec_data) < 10:
                continue
            # データをまとめる処理
            rec_data_len = len(rec_data)
            save_data = b"".join(rec_data)

            # データをNumpy配列に変換/時間軸を作成
            save_data = np.frombuffer(save_data, dtype="int16") / float((np.power(2, 16) / 2) - 1)
            while True:
                if savefolda.joinpath(savename+str(cnt)+".wav").exists():
                    cnt += 1
                else:
                    break
            sf.write(savename+str(cnt)+".wav", save_data, samplerate)
            voice_str = transform_audio_to_string.to_string(savename+str(cnt)+".wav")
            Path(savename+str(cnt)+".wav").unlink(missing_ok=True)
            voise_in = False
            rec_data = []
            silent_cnt = 0 
            if voice_str == "":
                continue
            res = responce_chatGPT.chat(voice_str)
            res_roman = transform_japanese_to_roman.convert_to_roman(res) 
            
            
    except KeyboardInterrupt:
        break

audiostop(audio,stream)


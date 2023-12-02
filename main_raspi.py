from lib import responce_chatGPT
from lib import transform_audio_to_string
from lib import transform_japanese_to_roman
from lib.speak import text2speech
import pyaudio
import numpy as np
import soundfile as sf
from pathlib import Path
from serial import Serial
from time import time,sleep
import sys
import RPi.GPIO as GPIO

def switch_callback(gpio_pin):
	global move, move_time,move_start_time
	move = not move
	if move == True:
		GPIO.output(mortor_pin, True)
		move_start_time = time.time()
	else:
		GPIO.output(mortor_pin, False)
		move_time += time.time() - move_start_time
	print("コールバック",gpio_pin)


# from Pysound_Error_hider import noalsaerr
"""https://niyanmemo.com/335/"""

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

# モーター関連
move = False
move_time = 0
move_start_time = 0
# PIN関連
speaker_a_pin = 22
mortor_pin = 24
GPIO.setmode(GPIO.BOARD)
GPIO.setup(mortor_pin, GPIO.OUT)
GPIO.setup(speaker_a_pin, GPIO.IN)
GPIO.add_event_detect(speaker_a_pin, GPIO.FALLING,bouncetime=100)
GPIO.add_event_callback(speaker_a_pin, switch_callback) #スイッチ入力端子の状態をcallbackのトリガとして指定します。    

savefolda = Path("lib")

savename = "rec"
samplerate = 44100
fs = 1024

if savefolda.exists() == False:
    savefolda.mkdir()

(audio,stream) = audiostart()
rec_data = []
cnt =0
silent_cnt = 0
voise_in = False

model = text2speech.DEVICE
ts = text2speech(model=model)

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
            res_romans = res_roman.split('。')
            for res_romas in res_romans:
                ts.write(res_roman)
            GPIO.cleanup()
                    
            
    except KeyboardInterrupt:
        break

audiostop(audio,stream)


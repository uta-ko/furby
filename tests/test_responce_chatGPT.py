from lib import responce_chatGPT
import time

def test_chat():
    audio_string = "こんにちは"
    res = responce_chatGPT.chat(audio_string)
    assert res != ""
    return

def test_chat_time():
    audio_string = "こんにちは"
    start_time = time.time()
    res = responce_chatGPT.chat(audio_string)
    end_time = time.time()
    print("spend time: ",end_time-start_time)
    assert res != ""
    return
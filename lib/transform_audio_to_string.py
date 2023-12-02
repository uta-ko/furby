# https://self-development.info/python%E3%81%A7%E9%9F%B3%E5%A3%B0%E3%81%8B%E3%82%89%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%81%B8%E5%A4%89%E6%8F%9B%E3%80%90speechrecognition%E3%80%91/
import speech_recognition as sr

def to_string(audiofile):
    r = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = r.record(source)
    try:  
        text = r.recognize_google(audio, language='ja-JP')
    except:
        text = ""
    print(text)
    return text


# Author: Baris Parlan - @bparlan
# Purpose: Wiki Summarizer Voice Assistant
# Created: 22.04.2018
# regina.py

"""
tags: reasoning logical behaviour evaluation algorithmic critical thinking opensource

platforms:
1. pc
2. mobile
3. web
4. car

resources:
- http://thepeakperformancecenter.com/educational-learning/thinking/critical-thinking/
- http://thepeakperformancecenter.com/educational-learning/thinking/blooms-taxonomy/

question reference:
https://i.pinimg.com/originals/3f/b0/21/3fb021de640b63861e27db09abc84f1e.jpg

TODO: Course https://www.udemy.com/cart/subscribe/course/808422/

packaging - https://python-packaging.readthedocs.io/en/latest/minimal.html
nltk - sentiment analysis
chatbot:
    rasa.stack - https://rasa.com/products/rasa-stack
    bot.press - https://botpress.io/
    bot framework - http://botframework.com/
    project ana - https://github.com/Kitsune-tools/ProjectAna
    wit.ai - https://wit.ai/
    api.ai - https://dialogflow.com/
docker
source search - wikipedia
pywsd - https://github.com/alvations/pywsd
networkx - mindmap logical graph
tts & stt
brain:
    wikipedia
    tvtropes - pop culture wiki
data:
    sql database?
    postgre sql
    aws
    data_tvtropes 3.2gb
        https://github.com/ricardojmendez/tropology
        https://mega.co.nz/#!EhZxhBhK!lT38KiMhGxTbjGKD6tJuimc48Tay4ILkEt70evgeM7c
joke
gensim?
web:
    django - https://www.djangoproject.com/
    flask - http://flask.pocoo.org/extensions/
    gunicorn - https://gunicorn.org/
Phase 1.
    Perspective to "Love, Death & Robots" with Regina.
    imdb api
    tvtropes api
"""



import settings # settings.py holds apikey variable.
import speech_recognition as sr # https://realpython.com/python-speech-recognition/
import os
from sys import byteorder
from array import array
from struct import pack
from multiprocessing import Process # https://stackoverflow.com/questions/2846653/how-to-use-threading-in-python#28463266

import time

import pyaudio
import wave

import wikipedia
# pip install wikipedia
import pyttsx3

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

script_dir = os.path.dirname(__file__)
wav_location = script_dir + "/demo.wav"

busy = False

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    #r = trim(r)
    #r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    print("Wav Recorded: " + path)

def speech_to_text():
    r = sr.Recognizer()
    harvard = sr.AudioFile(wav_location)
    with harvard as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    type(audio)

    # wav_text = r.recognize_google(audio)
    wav_text = r.recognize_google(audio, language="tr-TR")
    os.remove(wav_location) # delete wav file
    print("Wav's text: " + wav_text)
    return wav_text

def search_in_wiki(keyword):
    wikipedia.set_lang("en")
    tts_text = str(wikipedia.summary(keyword, sentences=1))
    return tts_text

def text_to_speech(to_be_read):
    engine = pyttsx3.init()
    engine.setProperty('rate',120)  #120 words per minute
    engine.setProperty('volume',0.9)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(to_be_read)
    engine.runAndWait()
    engine.stop()

def listen():
    print("I'm listening...")
    
    record_to_file(wav_location)
    busy == True
    query = speech_to_text()

    if(query == "Regina"):
        text_to_speech("Yes Master!")
        print("Yes Master!")

    text_to_speech("I am searching for " + query)
    text_to_speech(search_in_wiki(query))

    busy == False

def timer():
    start = time.time()
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    while busy == False:
        listen() # BAŞLATIYOR
        # TODO: search_image(sentence - keyword):
        #       search > download & save > while playing audio - play slideshow
        
        # TODO: while playing audio - write text to screen
        
        # TODO: define main functions search(other functions)
        # TODO: function 
        
        # TODO: Listen for "Regina", response "Yes master", and wait for commands.
        # TODO: List available commands / functions.

        # TODO: jsonstore offers a free and secured JSON-based cloud datastore for small projects https://www.jsonstore.io/
        # TODO: Factcheck of news
"""

* Speech Recognition
  [Wit.ai](https://github.com/wit-ai/pywit)
  https://realpython.com/python-speech-recognition/
* [Wikipedia](https://github.com/goldsmith/Wikipedia) - Get data
* [NLTK](https://github.com/nltk/nltk) - Summarize Wiki
* Text-to-speech
  https://deparkes.co.uk/2017/06/30/python-text-speech/
  https://pythonprogramminglanguage.com/text-to-speech/
  Sapi to play
  Gtts to save
  [gTTS](https://github.com/pndurette/gTTS)

RAP PART:
https://www.rappad.co/songs-about/
https://www.rhymebuster.com/rapgenerator
http://rapscript.net/
https://melobytes.com/app/melobytes
http://deepbeat.org/
https://genius.com/discussions/155749-Rap-generator
http://writerbot.com/lyrics

- Generate lyrics:
- Generate beat:
- Generate melody from lyrics: https://melobytes.com/app/melobytes
- Generate AVS milkdrop - python audio visualizer

def record_voice():
    # question["voice_question"] = str(input("Whats your question? "))
    # print("voice_question recorded")

def analysis_question():
    question["texts"] = question["question"].split()
    question["keyword"] = question["texts"][0]
    print("Words analysis done.\nKeyword: %s \nOther words:" % (question["keyword"]))
    question["duration"] = len(question["keyword"])
    for items in question["texts"]:
        print(items)

def calculate_word_count():
    print("Word count of question: %s" % (question["duration"]))
    question["kelime_sayisi"] = question["duration"]

def research_summary():
    input = record_voice()
    speech_to_text()
    analysis_question()
    search_keyword_on_web()
    save_results()
    calculate_word_count()
    save_answer()
    text_to_speach()
    read()

# research_summary()
"""

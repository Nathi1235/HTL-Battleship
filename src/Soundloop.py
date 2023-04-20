"""
die .wav files sind zu groß d.h. sie werden in der schule ausgetauscht
"""



import threading
import winsound

def soundtrack():
    while True:
        filename = 'Resources\Sound\Bmark3.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)
        filedings = 'Resources\Sound\Ctruce3.wav'
        winsound.PlaySound(filedings, winsound.SND_FILENAME)
        
        
def oneshipleft():
    filename= 'Resources\Sound\alarm.wav'
    while True:
        winsound.PlaySound(filename, winsound.SND_FILENAME)

        

def start_soundtrack():
    soundtrack_thread = threading.Thread(target=soundtrack)
    soundtrack_thread.start()


def start_oneshipleft():
    oneshipleft_thread = threading.Thread(target=oneshipleft)
    oneshipleft_thread.start()
"""
die .wav files sind zu groß d.h. sie werden in der schule ausgetauscht
"""



import threading
import winsound

def soundtrack():
    while True:
        filename = 'Bmark3.wav'
        winsound.PlaySound(filename, winsound.SND_FILENAME)
        filedings = 'Ctruce3.wav'
        winsound.PlaySound(filedings, winsound.SND_FILENAME)
        
        
def start_soundtrack():
    soundtrack_thread = threading.Thread(target=soundtrack)
    soundtrack_thread.start()
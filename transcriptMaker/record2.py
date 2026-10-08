"""
Once the audio is transcribed go to 
https://anki-decks.com/deck/create_deck_general_knowledge/ 
to turn it into flashcards

NOTE
NEED TO KEEP SOME FRAMES FROM THE END FOR CONTEXT FOR THE NEXT ITERATION OF TRANSCRIPTION
"""

import pyaudio
import wave
from transcribe import Transcriber
from time import perf_counter
from multiprocessing import Process, Queue
from datetime import datetime



#variables for the transcript file
now = datetime.now()
time = f"Y{now.year}M{now.month}D{now.day}_{now.hour}%{now.minute}%{now.second}"
outputFilePath = f"Python stuff\\transcriptMaker\\transcripts\\transcript_{time}.txt"

#setting up the transcriber
tr = Transcriber(
    model_size="turbo",
    device="cpu",
    compute_type="int8",
    outputFilePath=outputFilePath
)

#setting up the audio stream to record audio
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=2048
)
frames = []



def transcribe(q = Queue):
    """
    Saves frames and asks transcriber to transcribe it
    """

    #setting up the transcript file
    try:
        with open(outputFilePath, "w") as file:
            file.write(f" TRANSCRIPT START -- {time}")
    except FileExistsError:
        print("File already exists")
    
    while True:
        #gets frames from queue
        frames = q.get()
        
        #stops the program
        if frames == "STOP":
            break

        #saves frames
        soundFile = wave.open("Python stuff\\transcriptMaker\\temp.wav", "wb")
        soundFile.setnchannels(1)
        soundFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        soundFile.setframerate(44100)
        soundFile.writeframes(b"".join(frames))
        soundFile.close()

        #transcribes resulting audio
        tr.transcribe(
            filepath="Python stuff\\transcriptMaker\\temp.wav",
            batch_size=16,
            chunk_length=30
        )

def main():
    """
    Records and transcribes in 5min intervals
    """
    
    global frames

    #sets up the queue and multiprocessing
    q = Queue()
    st = Process(target=transcribe, args=(q,))
    st.start()

    print("Recording\npress ctrl+c to stop")

    #recording and putting audio frames into the queue
    try:
        start = perf_counter()
        while True:
            if perf_counter()-start >= 300: #every 5 minutes it will put the frames into the queue
                q.put(frames.copy())
                frames.clear()
                start = perf_counter()
                
            #reads the audio stream and stores the audio frames
            data = stream.read(2048, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        #if there is a keyboard interrupt it will stop the audio stream and tell the queue to shut down
        print("Recording stopped")
        q.put("STOP")
        stream.stop_stream()
        stream.close()
        audio.terminate()



if __name__ == "__main__":
    main()
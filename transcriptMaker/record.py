import pyaudio
import wave

class Recorder:
    def __init__(self, 
                 format, 
                 channels: int, 
                 rate: int, 
                 frames_per_buffer: int):
        self.audio = pyaudio.PyAudio()
        self.__format = format
        self.__channels = channels
        self.__rate = rate
        self.__frames_pb = frames_per_buffer

    def record(self):
        """
        Records frames of audio
        """

        stream = self.audio.open(
            format=self.__format,
            channels=self.__channels,
            rate=self.__rate,
            input=True,
            frames_per_buffer=self.__frames_pb
        )
        
        frames = []

        print("Recording\npress ctrl+c to stop")

        try:
            while True:
                data = stream.read(self.__frames_pb, exception_on_overflow=False)
                frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        return frames

    def writeFile(self, 
                  frames: list, 
                  directory: str, 
                  filename: str):
        """
        Creates a wav file from frames of audio
        """
        
        soundFile = wave.open(f"{directory}\\{filename}", "wb")
        soundFile.setnchannels(self.__channels)
        soundFile.setsampwidth(self.audio.get_sample_size(self.__format))
        soundFile.setframerate(self.__rate)
        soundFile.writeframes(b"".join(frames))
        soundFile.close()

recorder = Recorder(
    format=pyaudio.paInt16, 
    channels=1,
    rate=44100, 
    frames_per_buffer=2048
    )

frames = recorder.record()

recorder.writeFile(
    frames=frames, 
    directory="transcriptMaker", 
    filename="output.wav"
    )
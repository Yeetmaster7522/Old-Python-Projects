from faster_whisper import WhisperModel, BatchedInferencePipeline
from time import perf_counter

class Transcriber():
    def __init__(self, model_size, device, compute_type, outputFilePath):
        """
        Sets up the transcribing model and the transcript file
        """

        #setting up the model
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        self.batched_model = BatchedInferencePipeline(model=self.model)
        self.outputFilePath = outputFilePath
    
    def transcribe(self, filepath, batch_size, chunk_length):
        """
        Transcribes given audio from filepath and returns the entire transcript
        """

        #transcribing
        segments, info = self.batched_model.transcribe(
            filepath,
            batch_size=batch_size,
            chunk_length=chunk_length,
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 500,
                "speech_pad_ms": 400
            }
        )

        print(f"Transcription starting. {info.language} language: {info.language_probability}%")
        start = perf_counter()

        #going through each segment of the transcription, processing it, and appending the result to the transcript
        for segment in segments:
            print(f"Processing {segment.start} -> {segment.end}...")
            self.append(segment.text)

        #tells user transcription has stopped
        print(f"Transcription end. Transcription took {perf_counter()-start}s")
    
    def append(self, text):
        """
        Appends text to the file
        """

        with open(self.outputFilePath, "a") as file:
            file.write(f"{text}\n")



if __name__ == "__main__":
    #Testing the class
    pass
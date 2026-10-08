from gpt4all import GPT4All
from time import perf_counter as time

#https://docs.gpt4all.io/gpt4all_python/home.html#load-llm

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", device="cpu")
output = ""
lineCount = 5

with open("Python stuff\\transcriptMaker\\transcript.txt", "r") as file:
    transcript = file.readlines()

print("Task starting")
start = time()
t1 = 0
t2 = 0
t3 = 0

for x in range(0, len(transcript), lineCount):
    lines = transcript[x:x+lineCount]
    prompt = f"""
        You are a teacher creating flashcards for Year 11 students from a transcript of your class.

        Based on the transcript below, generate at least 5 flashcards. Each flashcard should have this specific structure:
        Q: [question]
        A: [answer]

        Focus on definitions, distinctions, and key ideas.
        Do not number the flashcards. Do not say "Flashcards:" at the start.
        
        Transcript:
        {"".join(lines)}
        """

    currentTime = time()-start
    print(f"Task {x/len(transcript)*100}% done. Current runtime: {currentTime}s / {(currentTime-t3)-(t2-t1)}s") #time difference thing is currently not working

    response = model.generate(
        prompt,
        max_tokens=256
        )
    output += f"\n{response}"
    print(response)

    t1=t2
    t2=t3
    t3=time()-start

print(f"Flashcard generation took {time()-start}")

flashcards = [line for line in output]
print(flashcards)

# with open("flascards.txt", "w") as file:
#     file.write()
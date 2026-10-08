#https://www.youtube.com/watch?v=CkkjXTER2KE
""",
    {
      "question": "",
      "answer": ""
    }"""
import json
from difflib import get_close_matches
import os
import pywhatkit as kit
import wikipedia
import requests
from bs4 import BeautifulSoup

script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

knowledge_base_location = os.path.abspath("knowledge_base.json")

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
    return data
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
def find_best_match(user_question: str, questions: list[str]) -> str:
    matches: list = get_close_matches(user_question, questions, n=2, cutoff=0.6)
    return matches[0] if matches else None
def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
def delete_knowledge_base():
    print("DEL")
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base(knowledge_base_location)
    while True:
        user_input: str = input("You: ")
        if user_input.lower() == "!quit":
            break

        best_match: str = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    
        if "!play" in user_input.lower():
            video = user_input.replace("!play ", "")
            kit.playonyt(video)
        elif "!search" in user_input.lower():
            user_input = user_input.replace("!search", "")
            search = user_input
            print("Searching")
            try:
                info = wikipedia.summary(search, 4)
            except Exception as e:
                print(e)
                url = f"https://www.google.com/search?q={search}"
                req = requests.get(url)
                soup = BeautifulSoup(req.text, "html.parser")
                info = soup.find("div", class_="BNeawe").text
            print(info)
        elif "!open" in user_input.lower():
            filename = os.path.abspath("jarvis33.py")
            os.system("start " + knowledge_base_location)
        elif "!delete" in user_input.lower():
            user_deletion = user_input.replace("!delete", "")
            delete_knowledge_base(user_deletion)
            
        elif best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer \n'!skip' to skip \n'!search' to search: ")
            if new_answer.lower() == "!search":
                search = user_input
                print("Searching")
                url = f"https://www.google.com/search?q={search}"
                req = requests.get(url)
                soup = BeautifulSoup(req.text, "html.parser")
                info = soup.find("div", class_="BNeawe").text
                print(info)
                knowledge_base["questions"].append({"question": user_input, "answer": info})
                save_knowledge_base("knowledge_base.json", knowledge_base)
            elif new_answer.lower() != "!skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank You! I learned a new response!")

if __name__ == "__main__":
    chat_bot()
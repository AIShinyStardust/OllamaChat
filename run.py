import sys
import os
import datetime
import json

from chat import *

MODEL = sys.argv[1]
SYS_PROMPT = sys.argv[2]
MAX_LENGTH = int(sys.argv[3])

@staticmethod
def printToFile(file:str, msg:str):
    logsFolder = "./logs"
    os.makedirs(logsFolder, exist_ok=True)
    folderName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fullPath = os.path.join(logsFolder, folderName)
    os.makedirs(fullPath, exist_ok=True)
    print(f"Folder '{fullPath}' Created")
    path = os.path.join(fullPath, file)
    with open(path, "w") as archivo:
        if isinstance(msg, list):
            archivo.write(json.dumps(msg, indent=2, ensure_ascii=False))
        else:
            archivo.write(msg)
    return

if __name__ == "__main__":
    chat = Chat(MODEL, SYS_PROMPT, MAX_LENGTH)
    while True:
        prompt = input("You: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Good bye!")
            break
        print(f"\n{MODEL}: {chat.doChat(prompt)}\n")
    printToFile("chatLog.json", chat.getChatHistory())


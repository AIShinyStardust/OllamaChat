import sys
import os
import datetime
import json

from chat import *

MODEL = sys.argv[1]
SYS_PROMPT = sys.argv[2]
MAX_LENGTH = int(sys.argv[3])


if __name__ == "__main__":
    chat = Chat(MODEL, SYS_PROMPT, MAX_LENGTH)
    while True:
        prompt = input("You: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Good bye!")
            break
        print(f"\n{MODEL}: {chat.doChat(prompt)}\n")
    chat.printToFile("Chat1")


import sys
import os
import datetime
import json

from aiss_ollama_chat.chat import Chat

MODEL = sys.argv[1]
SYS_PROMPT = sys.argv[2]
MAX_LENGTH = int(sys.argv[3])

def main():
    chat = Chat(MODEL, SYS_PROMPT, MAX_LENGTH)
    while True:
        prompt = input("You: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Good bye!")
            break
        print(f"\n{MODEL}: {chat.doChat(prompt)}\n")
    chat.printToFile("Chat1")
    return

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Run: ollama-chat <modelo> <prompt_sistema> <longitud_maxima>")
        print("Example: aiss_ollama_chat gemma3:12b-it-q8_0 'sysPrompt.txt' 20")
        sys.exit(1)
    main()

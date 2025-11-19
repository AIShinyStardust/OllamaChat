import sys
import argparse
import os
import datetime
import json

from aiss_ollama_chat.chat import Chat

def main():
    parser = argparse.ArgumentParser(
        description='OpenAPI user-assistant chat app.',
        epilog='Example: ollama-chat gemma3:12b-it-q8_0 sysPrompt.txt 20'
    )
    
    parser.add_argument('model', help='Model to use')
    parser.add_argument('sysPrompt', help='Plain text file with the system prompt')
    parser.add_argument('--maxLength', '-l', type=int, default=20,
                    help='Maximum context lenght (default: 20)')
    parser.add_argument('--userName', '-u', type=str, default="User",
                    help='User name (default: "User")')
    parser.add_argument('--prevContext', '-c', type=str, default=None,
                    help='Txt file path with previous chat context (default: None)')

    args = parser.parse_args()

    chat = Chat(args.model, args.sysPrompt, args.maxLength, args.userName, args.prevContext)
    while True:
        prompt = input(f"{chat.userName}: ")
        try:
            msg = chat.chat(prompt)
            if msg == None:
                print("Good bye!")
                break
            print(msg)
        except Exception as e:
            print(f"{e}\n")
    chat.makeBackup()
    return

if __name__ == "__main__":
    main()

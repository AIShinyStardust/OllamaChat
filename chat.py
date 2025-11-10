import ollama
import datetime
import json
import re

class Chat:

    @staticmethod
    def strMsg(event_type:str, content:str) -> dict[str, str]:
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'role': event_type,
            'content': content
        }

    def __init__(self, model:str, sysPrompt1:str, maxChatLenght:int=20):
        self.model:str = model
        self.chatHistory:dict[str, str] = []
        self.sysPrompt:str = ""
        self.maxChatLenght:int = maxChatLenght
        
        with open(sysPrompt1, "r") as archivo:
            self.sysPrompt = archivo.read()
    
    def __chatOllama(self, prompt:str) -> str:
        self.chatHistory.append(self.strMsg("user", prompt))
        response = ollama.chat(self.model, messages=[{"role": "system", "content": self.sysPrompt}] + self.chatHistory[-self.maxChatLenght:])
        msg = response['message'].content
        self.chatHistory.append(self.strMsg("assistant", msg))
        return msg
    
    def doChat(self, prompt:str) -> str:
        return self.__chatOllama(prompt)
    
    def getChatHistory(self) -> str:
        return self.chatHistory
    

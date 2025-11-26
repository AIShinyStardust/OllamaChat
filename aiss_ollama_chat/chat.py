import os
import time
import ollama
import datetime
import re
import pyperclip

from aiss_ollama_chat.fileIO import FileIO

class Chat:
    @staticmethod
    def addClipBoardIfNeeded(text):
        index = text.find('@@')
        if index < 0:
            return text
        clipBoard = repr(pyperclip.paste())[1:-1]
        out = f"{text[:index]}\n```\n{clipBoard}\n```\n{text[index + len('@@'):]}"
        return out
    
    @staticmethod
    def strMsg(event_type:str, content:str, addDateTimeToContent:bool=False) -> dict[str, str]:
        dateTime = datetime.datetime.now().isoformat()
        return {
            'timestamp': dateTime,
            'role': event_type,
            'content': f"{dateTime}\n{content}" if addDateTimeToContent else content
        }

    def __init__(self, model:str, sysPrompt:str, maxChatLength:int=20, userName:str="user", prevContext:str=None, addDateTimeToPrompt:bool=False, sysPromptDropTurn:int=None):
        self.model:str = model
        self.sysPrompt:str = ""
        self.maxChatLength:int = maxChatLength
        self.userName:str = userName
        self.addDateTimeToPrompt:bool = addDateTimeToPrompt
        self.sysPromptDropTurn:int = sysPromptDropTurn
        self.chatHistory:dict[str, str] = []
        self.operations = {
            "save": self._handleSave,
            "restore": self._handleRestore,
            "rewind": self._handleRewind,
            "print": self._handlePrint
        }
        try:
            with open(sysPrompt, "r") as archivo:
                self.sysPrompt = archivo.read()
            if prevContext:
                self.chatHistory = FileIO.deserializeDict(prevContext)
        except Exception as e:
            return
    
    def doChat(self, prompt:str) -> str:
        self.chatHistory.append(self.strMsg("user", prompt, True and self.addDateTimeToPrompt))
        if self.sysPromptDropTurn:
            if len(self.chatHistory) < (2*self.sysPromptDropTurn):
                response = ollama.chat(self.model, messages=[{"role": "system", "content": self.sysPrompt}] + self.chatHistory[-self.maxChatLength:])
            else:
                response = ollama.chat(self.model, messages=[{"role": "system", "content": " ... "}] + self.chatHistory[-self.maxChatLength:])
        else:
            response = ollama.chat(self.model, messages=[{"role": "system", "content": self.sysPrompt}] + self.chatHistory[-self.maxChatLength:])
        msg = response['message'].content
        self.chatHistory.append(self.strMsg("assistant", msg))
        return msg
    
    def chat(self, prompt: str) -> str:
        try:
            for operation, handler in self.operations.items():
                if prompt.startswith(operation):
                    return handler(prompt)
            return f"{self.model}: {self.doChat(Chat.addClipBoardIfNeeded(prompt))}\n\n"
        except Exception as e:
            raise Exception(f"{e}\\n")
        return

    def _handleSave(self, prompt: str) -> str:
        if prompt.startswith("save:"):
            path = prompt[len("save:"):].strip()
            FileIO.serializeDict(path, self.chatHistory)
            return f"-- serialized to {path} --\n\n"
        else:
            FileIO.serializeDict("./context.json", self.chatHistory)
            return "-- serialized to ./context.json --\n\n"

    def _handleRestore(self, prompt: str) -> str:
        if prompt.startswith("restore:"):
            path = prompt[len("restore:"):].strip()
            self.chatHistory = FileIO.deserializeDict(path)
            return f"-- restored from {path} --\n\n"
        else:
            self.chatHistory = FileIO.deserializeDict("./context.json")
            return "-- restored from ./context.json --\n\n"

    def _handleRewind(self, prompt: str) -> str:
        if prompt.startswith("rewind:"):
            amount = int(prompt[len("rewind:"):].strip())
            self.rewind(amount)
            return f"-- rewind: {amount} --\n\n"
        else:
            self.rewind()
            return "-- rewind: 1 --\n\n"
        
    def _handlePrint(self, prompt:str) -> str:
        if prompt.startswith("print:"):
            prompt = prompt[len("print:"):].strip()
            if prompt.startswith("system"):
                return f"-- System prompt: {self.sysPrompt}\n\n"
            elif prompt.startswith("chat"):
                return f"-- Chat History --\n{self.getChatHistoryFormatted()}\n-- Chat History End --\n\n"
        else:
            return f"-- System prompt: {self.sysPrompt}--\n\n"
    
    def rewind(self, turns=1) -> str:
        if turns < 0:
            raise ValueError(f"Rewind parameter `turns` cannot be a negative value. Request: {turns}")
        self.chatHistory = self.chatHistory[:-min(self.parseTurnToIndex(turns), len(self.chatHistory))]

    def parseTurnToIndex(self, t) -> int:
        return t * 2

    def parseIndextoTurn(self, i) -> int:
        return i // 2

    def getCurrentTurn(self) -> int:
        return len(self.chatHistory) // 2
    
    def getLastContextMsg(self):
        if len(self.chatHistory) == 0:
            return ""
        else:
            return self.chatHistory[-1]['content']

    def getChatHistoryFormatted(self) -> str:
        formattedStrings = []
        i = 0
        for dictionary in self.chatHistory:
            turnNum = self.parseIndextoTurn(i)
            role = dictionary.get("role", "")
            content = dictionary.get("content", "")
            if role == "user":
                formattedString = f"Turn {turnNum} - {self.userName}: {content}"
            else:
                formattedString = f"Turn {turnNum} - {self.model}: {content}"
            formattedStrings.append(formattedString)
            i += 1
        return "\n\n".join(formattedStrings)

    def makeBackup(self, folder:str = None, suffix:str = ""):
        logsFolder = "./logs"
        os.makedirs(logsFolder, exist_ok=True)
        if folder:
            folderName = f"{folder}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        else:
            folderName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fullPath = os.path.join(logsFolder, f"{folderName}{suffix}")
        os.makedirs(fullPath, exist_ok=True)
        print(f"Folder '{fullPath}' Created")
        FileIO.serializeDict(os.path.join(fullPath, "chat.json"), self.chatHistory)
        FileIO.serializeDict(os.path.join(fullPath, "params.log"), {
                "app":"aiss_ollama_chat",
                "model":self.model,
                "maxChatLength":self.maxChatLength,
                "userName":self.userName,
                "sysPrompt":self.sysPrompt
            })
        return

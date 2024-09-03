from geminiBot import GeminiBot
import time
import pyperclip
import keyboard
import config


class ChatInteractor:
    def __init__(self):
        self.memory = dict()
        self.memory['messages'] = []
        self.memoryLength = 0
        self.contextLength = 1000
        self.gemini = GeminiBot()

    def tokenize(self, message):
        return len(message['role']) // 5 + 1 + len(message['content']) // 5 + 1

    def formatMessage(self, message):
        if "[CHAT]" in message:
            message = message.replace("\n", "")
            message = message[message.find("[CHAT]") + 6:]
        if 'internal error' in message:
            message = "Помогите... Мне..."
        return message

    def read_message(self, message, source):
        message = self.formatMessage(message)
        entry = {}
        entry['role'] = source
        entry['content'] = message
        self.memory['messages'].append(entry)
        self.memoryLength += self.tokenize(entry)
        while self.memoryLength > self.contextLength:
            self.memoryLength -= self.tokenize(self.memory['messages'][0])
            self.memory.pop(0)

    def send_message(self, message, source):
        keyboard.press_and_release('t')
        time.sleep(0.1)
        buffer = pyperclip.paste()
        pyperclip.copy(message)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)
        pyperclip.copy(buffer)
        keyboard.press_and_release('enter')

    def split_text(self, text, block_size):
        blocks = []
        start = 0
        while start < len(text):
            blocks.append(text[start:start + block_size])
            start += block_size
        return blocks

    def process_command(self, command):
        if "[require_llm_message]" in command:
            answer = self.gemini.generate_message(self.memory)
            self.read_message(answer, config.godName)
            answer_list = answer.split('@')
            message_blocks = self.split_text(answer_list[0], 256)
            for message_block in message_blocks:
                self.send_message(message_block, config.godName)
            for command in answer_list[1:]:
                self.send_message("@" + command, config.godName)
        else:
            nick = "[CHAT]  Hero VaniusKon"
            #if not nick in command:
            self.read_message(command, "Мир")

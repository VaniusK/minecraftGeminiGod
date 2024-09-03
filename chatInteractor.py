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
        self.contextLength = 4000
        self.gemini = GeminiBot()

    def tokenize(self, message):
        return len(message['role']) // 5 + 1 + len(message['content']) // 5 + 1

    def formatMessage(self, message):
        message = message[message.find("[llm_read_this]") + len("[llm_read_this]") + 1:]
        print(message)
        message_split = message.split(" ")
        nick = message_split[0]
        text = ' '.join(message_split[1:])
        return nick, text

    def read_message(self, message, source):
        entry = {}
        entry['role'] = source
        entry['content'] = message
        self.memory['messages'].append(entry)
        self.memoryLength += self.tokenize(entry)
        while self.memoryLength > self.contextLength:
            self.memoryLength -= self.tokenize(self.memory['messages'][0])
            self.memory.pop(0)

    def send_message(self, message, source):
        if 'internal error' in message:
            message = "Помогите... Мне..."
        keyboard.press_and_release('t')
        time.sleep(0.1)
        buffer = pyperclip.paste()
        pyperclip.copy(message)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)
        pyperclip.copy(buffer)
        keyboard.press_and_release('enter')
        time.sleep(0.5)

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
            message_list = answer_list[0].split('\\n')
            for message in message_list:
                message_blocks = self.split_text(message, 256)
                for message_block in message_blocks:
                    self.send_message(message_block, config.godName)
            for command in answer_list[1:]:
                self.send_message("@" + command, config.godName)
        else:
            nick, message = self.formatMessage(command)
            self.read_message(message, nick)

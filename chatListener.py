import os
import time
from chatInteractor import ChatInteractor
import config


class ChatListener():
    def __init__(self):
        self.log_file_path = config.log_file_path
        if not os.path.exists(self.log_file_path):
            print(f"Файл {self.log_file_path} не найден.")
            exit()
        self.interactor = ChatInteractor()

    def start_listening(self):

        last_message_time = time.time()
        with open(self.log_file_path, 'r', encoding='cp1251', errors='replace') as log_file:
            log_file.seek(0, os.SEEK_END)

            while True:
                time.sleep(0.1)
                if time.time() - last_message_time >= config.delay_between_messages:
                    self.interactor.process_command("[require_llm_message]")
                    last_message_time = time.time()
                line = log_file.readline()

                if not line:
                    continue
                if line[line.find("[CHAT]") + 8] in ['|', ' ', "\\", '?']:
                    continue
                if "[CHAT]" in line:
                    self.interactor.process_command(line)




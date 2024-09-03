from geminiInteractor import GeminiInteractor
import time
import config

class GeminiBot:
    def __init__(self):
        self.interactor = GeminiInteractor()
        self.message_prompt = config.bot_message_prompt

    def generate_message(self, context):
        prompt = self.message_prompt + f"ПОСЛЕДНИЕ СОБЫТИЯ(Самые новые в конце): [[[{context}]]]"
        self.interactor.send_message(prompt)
        while self.interactor.is_generating():
            time.sleep(0.1)
        time.sleep(1)
        answer = self.interactor.get_last_message()
        return answer
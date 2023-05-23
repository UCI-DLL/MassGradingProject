import openai
import os
import docx2txt
import json
import time

from .writer import csv_write, exec_log_write
from datetime import datetime


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        exec_log_write(os.getenv("outcome_dir_path", None),
                       f"Total execution time of grading: {end - start} seconds.\n")
        return result

    return wrapper


class ChatGPTClient:
    def __init__(self, dir_path, temperature):
        self.dir_path = dir_path  # directory path of the selected essays
        self.msg_lst = []
        self.temp = temperature
        self.outcome_dir_path = os.path.join(
            self.dir_path,
            datetime.now().strftime(r"%Y-%m-%d %H-%M-%S")
        )
        os.environ["outcome_dir_path"] = self.outcome_dir_path
        self.init_instructions()

    def init_instructions(self):
        instruction_path = os.path.join(self.dir_path, "chatgpt_instruction.txt")
        with open(instruction_path, 'r', encoding='utf8') as f:
            actor_instruction = {
                "role": "system",
                "content": f.read()
            }
            self.msg_lst.append(
                actor_instruction
            )
            print(self.outcome_dir_path)
            exec_log_write(self.outcome_dir_path, actor_instruction)

    def chat(self, input_prompt) -> object:
        # Token limits
        if len(self.msg_lst) >= 3:
            self.msg_lst.pop()
            self.msg_lst.pop()

        # Question
        question = {
            "role": "user",
            "content": input_prompt
        }
        self.msg_lst.append(
            question
        )
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.msg_lst,
            temperature=self.temp
        )

        # Answer
        answer = response["choices"][0]["message"]  # role as 'assistant'
        self.msg_lst.append(answer)

        # log down Q&A
        exec_log_write(self.outcome_dir_path, question)
        exec_log_write(self.outcome_dir_path, answer)

        return answer

    @time_it
    def grading(self):
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith('.docx'):
                    file_path = os.path.join(root, file)
                    file_text = docx2txt.process(file_path)
                    file_text = "<<" + file_text + ">>"

                    exec_log_write(self.outcome_dir_path, f'[[Now grading {file}]]\n')
                    resp_msg = self.chat(file_text)
                    exec_log_write(self.outcome_dir_path, f'-----------------------')

                    resp_msg = resp_msg["content"]
                    print(resp_msg)

                    try:
                        resp_dict = json.loads(resp_msg.strip(","))  # transfer value type from str to dict
                    except:
                        # edge case: remove trailing comma
                        if resp_msg.startswith('\ufeff'):
                            resp_msg = resp_msg.split('\ufeff')[1]
                        resp_dict = json.loads(resp_msg.strip(","))

                    csv_data = {"name": file.split(sep='.')[0]}
                    csv_data.update(resp_dict)

                    # add essay column
                    csv_data["essay"] = file_text[2:-2]

                    csv_write(self.outcome_dir_path, csv_data)

    def get_outcome_dirname(self):
        return self.outcome_dir_path

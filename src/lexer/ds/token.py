import os

from utils.configs import Configs


class TokenLine():
    def __init__(self, word_content=None, word_type=None, token_type=None, token_content=None):
        self.word_content = word_content
        self.word_type = word_type
        self.token_type = token_type
        self.token_content = token_content

    def __str__(self):
        return f'{self.word_content}   <{self.token_type},{self.token_content}>'

    def input_raw_line(self, word_content, word_type):
        self.word_content = word_content
        self.word_type = word_type
        self._process_raw_line()

    def output_token_line(self):
        return f'{self.word_content}   <{self.token_type},{self.token_content}>'

    def _process_raw_line(self):
        if self.word_type == 'kW+IDN+4OP':
            if self.word_content in Configs.KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(Configs.KW)

            elif self.word_content in Configs.OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(Configs.OP)

            else:
                self.token_type = 'IDN'
                self.token_content = self.word_content

        elif self.word_type == 'OP':
            self.token_type = 'OP'
            self.token_content = self._get_token_id(Configs.OP)

        elif self.word_type == 'KW':
            self.token_type = 'KW'
            self.token_content = self._get_token_id(Configs.KW)

        elif self.word_type == 'SE+1KW+3OP':
            if self.word_content in Configs.KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(Configs.KW)

            elif self.word_content in Configs.OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(Configs.OP)

            elif self.word_content in Configs.SE:
                self.token_type = 'SE'
                self.token_content = self._get_token_id(Configs.SE)

            else:
                print(self.word_content)
                print("ERROR in _process_raw_line(), SE+1KW+3OP NOT FOUND")

        elif self.word_type == 'STRING':
            self.token_type = 'STRING'
            self.token_content = eval(self.word_content)

        elif self.word_type == 'INT':
            self.token_type = 'INT'
            self.token_content = self.word_content

        elif self.word_type == 'FLOAT':
            self.token_type = 'FLOAT'
            self.token_content = self.word_content

        else:
            print(self.word_type)
            print("ERROR in _process_raw_line(), NOT TYPE MATCH")

    def _get_token_id(self, token_type):
        for i, op in enumerate(token_type):
            if op == self.word_content:
                return i + 1


class TokenTable():
    def __init__(self):
        self.token_table = []

    def add_token_line(self, toke_line):
        self.token_table.append(toke_line)

    def print(self):
        for token_line in self.token_table:
            print(token_line)

    def save(self, test_name):
        file_name = 'token_table_' + test_name.split(os.path.sep)[1].replace(".sql", ".txt")
        save_path = os.path.join(Configs.dir_names['output'], "token_table", file_name)
        with open(save_path, 'w') as f:
            for token_line in self.token_table:
                f.write(token_line + '\n')

    def reset(self):
        self.token_table = []

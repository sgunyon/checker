import re
import ast

TIME = re.compile('time\=(.+?)\,')
MODULE = re.compile('module\=(.+?)\,')
TYPE = re.compile('type\=(.+?)\,')
ACTION = re.compile('action\={(.+?)\}')

class Parser():
    def __init__(self):
        self.dict_format = {
            'time' : '',
            'module' : '',
            'type' : '',
            'action' : ''
        }

    def parse_data(self, data):
        if re.search('Operation{', data) and not re.search('repair', data):
            self.time = TIME.search(data).group(1)
            self.module = MODULE.search(data).group(1)
            self.type = TYPE.search(data).group(1)
            self.action = ast.literal_eval(ACTION.search(data).group(1))

            self.dict_format = {
                'time' : self.time,
                'module' : self.module,
                'type' : self.type,
                'action' : self.action
            }

            return self.dict_format

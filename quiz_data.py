import requests
import numpy as np
import json

data_file = open('question_bank.json')
response = json.load(data_file)
question_data = response["vocabulary_quiz"]

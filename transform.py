import zipfile
import pandas as pd
import json
import re

pd.options.display.max_colwidth = 0

CONST = zip_source_data_file_path = 'data/chat_archive.zip'
CONST = json_contact_list_file_path = 'data/contact_names.json'
CONST = txt_archive_file_name = '_chat.txt'


def read_source_dataframe():
# create df from chat data in zip archive
    with zipfile.ZipFile(zip_source_data_file_path, 'r') as zip_ref:
        # Read the .txt file
        with zip_ref.open(txt_archive_file_name) as file:
            data = file.read().decode('utf-8')
            lines = data.strip().split('\n')
            source_dataframe = pd.DataFrame(lines, columns=["text"])
    
    return source_dataframe

def read_whatsapp_contacts():
    # create list of all names in contact_names.json for regex removal
    with open(json_contact_list_file_path, 'r', encoding='utf-8') as file:
        # Parse the JSON data into a Python list
        data_list = json.load(file)

    # return contact list with escaped characters
    return  [re.escape(value) for value in data_list]


def transform_data(original_dataframe):
# Regex patterns to exclude from the text messages
    df = original_dataframe

    patterns = [r'\[.*?\]',
                r'\r',
                r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F251]',
                r'\b(?:' + '|'.join(read_whatsapp_contacts()) + r')\b',
                r' : ',
                r'^\s+',
                r'sticker omitted']

    def apply_pattern(text, patterns):
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        return text

    # Apply the re.sub function using a lambda function to the 'text' column
    transformed_dataframe = df['text'].apply(lambda x: apply_pattern(x, patterns))

    return transformed_dataframe
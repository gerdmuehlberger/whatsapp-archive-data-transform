import zipfile
import pandas as pd
import json
import re

pd.options.display.max_colwidth = 0

zip_file_path = 'data/chat_archive.zip'
contact_list = 'data/contact_names.json'
txt_file_name = '_chat.txt'


# create df from chat data in zip archive
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Read the .txt file
    with zip_ref.open(txt_file_name) as file:
        data = file.read().decode('utf-8')
        lines = data.strip().split('\n')
        df = pd.DataFrame(lines, columns=["text"])


# create list of all names in contact_names.json for regex removal
with open(contact_list, 'r', encoding='utf-8') as file:
    # Parse the JSON data into a Python list
    data_list = json.load(file)

contact_list_escaped_values = [re.escape(value) for value in data_list]


# Regex patterns to exclude from the text messages

patterns = [r'\[.*?\]',
            r'\r',
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F251]',
            r'\b(?:' + '|'.join(contact_list_escaped_values) + r')\b',
            r' : ',
            r'^\s+',
            r'sticker omitted']

def apply_pattern(text, patterns):
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    return text

# Apply the re.sub function using a lambda function to the 'text' column
df['text'] = df['text'].apply(lambda x: apply_pattern(x, patterns))

# Display the DataFrame
print(df.head(20))

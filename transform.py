import zipfile
import pandas as pd
import re

# Path to the ZIP file
zip_file_path = 'data/chat_archive.zip'

# Name of the .txt file within the ZIP archive
txt_file_name = '_chat.txt'


# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Read the .txt file
    with zip_ref.open(txt_file_name) as file:
        # Read the file contents
        data = file.read().decode('utf-8')

        # Split the data into lines
        lines = data.strip().split('\n')

        # Create a DataFrame with one column
        df = pd.DataFrame(lines, columns=["text"])


# Regex pattern to match text within square brackets, including the brackets
pattern = r'\[.*?\]'

# Apply the re.sub function using a lambda function to the 'text' column
df['text'] = df['text'].apply(lambda x: re.sub(pattern, '', x))

# Display the DataFrame
print(df.head(10))

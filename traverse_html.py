import os

# Source: https://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string

prefixed = [filename for filename in os.listdir(
    'www/') if filename.startswith("index")]

print(prefixed)


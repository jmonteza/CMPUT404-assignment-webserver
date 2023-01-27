import os
from pathlib import Path

# If it is a directory, we redirect. Otherwise, we try to serve the file without empty extension

path = 'www/deep'

isExist = os.path.exists(path)

print("TRUE:", isExist)

isdir = os.path.isdir(path)

print("TRUE:", isdir)

path = 'www/deep/index.html'

isfile = os.path.isfile(path)

print("www/deep/index.html is file:", isfile)


path = Path(r'www/../../')

print(path.parent)
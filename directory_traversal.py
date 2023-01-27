import os

# https://stackoverflow.com/questions/45188708/how-to-prevent-directory-traversal-attack-from-python-code

path = '/www/hardcode/deep/../../../www/index.html'
safe_path = '/www/'
# print(os.path.abspath(path))
print(os.path.realpath(path))

print(os.path.realpath(path).startswith(safe_path))


# print(os.path.commonprefix((os.path.realpath(path), safe_path)))

# os.path.commonprefix((os.path.realpath(requested_path),safe_dir)) != safe_dir
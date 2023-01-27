from pathlib import Path

p = Path(r'/www/www/index.html')

print(p.parent)

print(p.parts)

p = Path(r'/deep/index.html')

print(p.parts)

p = Path(r'/deep/web/index.html')

print(p.parent)

print(p.parts)

print(p.name)
print("***************")

p = Path(r'/deep')

print(p.name)

print(len(str(p.name)))

print(len(str(p.suffix)))
# print("www" + str(p.parent) + "/" + str(p.name))

print("www" + str(p))

print("*******************\n")

p = Path(r'/../../../index.html')

print(p.parent)
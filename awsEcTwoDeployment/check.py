import re
a = re.sub(r'(-script\.pyw|\.exe)?$', '', "python worker.py")
print(a)
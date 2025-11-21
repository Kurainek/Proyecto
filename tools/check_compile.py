import pathlib
import py_compile
import sys

errors = []
for p in pathlib.Path('.').rglob('*.py'):
    s = str(p)
    if '.conda' in s or '__pycache__' in s:
        continue
    try:
        py_compile.compile(s, doraise=True)
    except Exception as e:
        errors.append((s, repr(e)))

if errors:
    print('COMPILE_ERRORS')
    for f, e in errors:
        print(f + ': ' + e)
    sys.exit(2)
else:
    print('COMPILE_OK')
    sys.exit(0)

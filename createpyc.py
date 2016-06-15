import py_compile
import glob

for file in glob.glob("*.py"):
        py_compile.compile(file)

print ("Success...!!!")

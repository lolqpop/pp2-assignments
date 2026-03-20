import os

file_name = "copy_example.txt"

if os.path.exists(file_name):
    os.remove(file_name)
    print("File deleted")
else:
    print("File does not exist.")
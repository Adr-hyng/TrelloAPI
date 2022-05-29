import os

directory = "C:/Users/Adrian/Documents/Adrian/School/2nd Semester/In Progress/My Modules"
subfolders = [ f.name for f in os.scandir(directory) if f.is_dir() ]

modules = []
for folder in subfolders:
    for index in range(4):
        print(f"{folder} - LP{index+1}")
        modules.append(f"{folder} - LP{index+1}")


with open("modules.txt", "w+") as file:
    for module in modules:
        file.write(str(module) + "\n")
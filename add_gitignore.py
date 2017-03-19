import os

def add_to_global():
    for file in os.listdir('./'):
        if file.__contains__('.gitignore'):
            exec_command = 'git config --global core.excludesfile ' + os.getcwd() + file
            print exec_command
            os.system(exec_command)

add_to_global()
os.chdir('Global')
add_to_global()

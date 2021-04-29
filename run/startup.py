import os, platform

current_os = platform.system()


def start_up():
    if current_os == 'Windows':
        os.system('color')

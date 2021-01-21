from os import system
from os.path import abspath

system(f'setx PATH "%PATH%;{abspath(r"Script")}"')

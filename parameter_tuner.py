import subprocess
import json
import random

win_dict = {'b':0,'r':0}

for i in range(10):
    command = 'python -m referee agent agent -v 1'
    command = 'python -m referee agent agent:RandomAgent -v 1'

    # Execute the command and capture the output
    result = subprocess.check_output(command, shell=True, text=True)

    # Split the output into lines
    lines = result.split("\n")

    # Get the last line of the output
    winner_line = lines[-3]  # The last line will be the second-to-last line because the last line will be an empty string
    turn_line = lines[-5]

    if 'BLUE' in winner_line:
        print("blue won after:", turn_line)
        win_dict['b']+=1
    else:
        print("red won after:", turn_line)
        win_dict['r']+=1

print(win_dict)
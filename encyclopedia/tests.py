from django.test import TestCase
from util import save_entry, get_entry, list_entries
import re
from sys import exit

# Create your tests here.
s = ["Felipe", "Tiago", "pedrO"]
t = input("Name: ")

if t in s:
    print(t)
    exit(0)


for i in s:
    if t.lower() in i.lower():
        print("True")
        print(f'Did you mean "{i}"?')
        break
    else:
        print("False")
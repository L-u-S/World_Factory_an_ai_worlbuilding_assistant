import os
import requests
import json

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.prompt import IntPrompt
from rich.prompt import Confirm
from rich.padding import Padding
from rich.style import Style
from rich.markup import escape

from config import Config



# SETUP
console = Console(width=100)
conf = Config()

# UI SETUP
if conf.black_on_white_style == True:
    os.system('color F0')
    style_used = conf.style_types['bow']

else:
    style_used = conf.style_types['default']



def add_input(text):
    console.print(Padding(f'{text}', (1, 2, 1, 3)))
    added_input = Prompt.ask() 
    return added_input



def add_inputs(text):
    inputs = []
    console.print(Padding(f'''{text} If that's all, and you want me to start generating a response, write: "ok":''', (1, 2, 1, 3)), style=style_used)
#   console.print(Padding(f'''{text} If that's all, and you want me to start generating a response, write: "ok":''', (1, 2, 1, 3)), style=conf.txt_style)
    while True:
        idea_input = Prompt.ask()
        if idea_input.lower() == "ok":
             inputs.append(' ')
             break
        elif idea_input.lower() == "skip":
            return ["skip"]
        else:            
            inputs.append(idea_input)
    return inputs


def random_words(number):
    random = requests.get(f'https://random-word-api.herokuapp.com/word?number={number}')
    return ', '.join(json.loads(random.text))



def printout(the_world, chapters, definitions, substitutions):
    try:
        console.print(Padding(the_world, (1, 2, 1, 3)), style=style_used)
    except: 
        pass
    
    try:
        for key, value in chapters.items():
            console.print(Padding(f'{key.upper()} {value}', (1, 2, 1, 3)), style=style_used)
    except:
        pass
    
    try:
        console.print(Padding(f'{definitions} {substitutions}', (1, 2, 1, 3)), style=style_used)
    except:
        pass    



def rollback(memory):
    console.print(Padding('How far should I roll back?', (1, 2, 1, 3)))
    world_number = IntPrompt.ask()
    world_number = -(world_number)
    try:
        console.print(Padding(memory[world_number], (1, 2, 1, 3)))
        if Confirm.ask('Do you want to make this world the primary one') == True:
            return (True, memory[world_number])
        else:
            return (False, '')
    except:
        console.print(Padding('Sorry, no such world! Try again.', (1, 2, 1, 3)), style=style_used)
        return (False, '')



def extract_data():
    console.print(Padding('What number does the file have (e.g. my_world_3.txt is number 3)?', (1, 2, 1, 3)), style=style_used)
    file_number = IntPrompt.ask() 
    app_path = os.getcwd()
    file_path = f"{app_path}\saved worlds\my_world_{file_number}.txt"
    try:
        with open(file_path, 'r') as file:
            saved_data = file.read()
            the_world = saved_data.split('------------------------')[0]
            chapters = saved_data.split('CHAPTERS: ')[1].split('------------------------')[0]
            definitions = saved_data.split('DEFINITIONS: ')[1].split('------------------------')[0]
            substitutions = saved_data.split('SUBSTITUTIONS: ')[1].split('------------------------')[0]
            memory = saved_data.split('MEMORY: ')[1].split('------------------------')[0]
            input_sum = saved_data.split('INPUT SUM: ')[1].split('------------------------')[0]
            return the_world[8:], chapters, definitions, substitutions, memory, input_sum
    except:
        console.print(Padding('No such file or other problem encountered.', (1, 2, 1, 3)), style=style_used)
        return False



def save_to_file(the_world, chapters, definitions, substitutions, memory, input_sum):
    memory_string = '\n'.join(memory)
    saving_world = f'''WORLD: {the_world}\n------------------------\n\
                       CHAPTERS: {json.dumps(chapters)}\n------------------------\n\
                       DEFINITIONS: {definitions}\n------------------------\n\
                       SUBSTITUTIONS: {substitutions}\n------------------------\n\
                       MEMORY: {json.dumps(memory)}\n------------------------\n\
                       INPUT SUM: {json.dumps(input_sum)}'''
    app_path = os.getcwd()
    subdir_path = os.path.join(app_path, "saved worlds")
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)
    x = 1
    file_path = os.path.join(subdir_path, f"my_world_{x}.txt")
    while os.path.exists(file_path):
        x += 1
        file_path = os.path.join(subdir_path, f"my_world_{x}.txt")
    with open(file_path, "w") as f:
        f.write(saving_world)
    console.print(Padding(f"Saved as: {file_path}", (1, 2, 1, 3)), style=style_used)



def get_aikey():
    app_path = os.getcwd()
    file_path = f"{app_path}/aikey.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            aikey = str(file.read())
            return aikey
    else:
        console.print(Padding("I'm sorry but I can't find the openai api key. Please provide it by \
                                placing it in config.openai_key, setting an envirnomental variable \
                                or placing it in aikey.txt file in the app folder.", (1, 2, 1, 3)))



# NOT USED
def split_description(description, split_word, index):
    try:
        output = description.split(split_word)[index]
        return output
    except:
        console.print("\n\n Something went wrong! Returning whole content. If it's bad don't save it!\n")
        return description

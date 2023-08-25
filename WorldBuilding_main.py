import openai
import json
import os

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.prompt import IntPrompt
from rich.prompt import Confirm
from rich.padding import Padding
from rich.style import Style


import combined_functions as c_f
from config import Config
import loose_prompts as l_p
import functions as func



# SETUP
conf = Config()
console = Console(width=100)

# UI SETUP
if conf.black_on_white_style == True:
    os.system('color f0')
    b_o_w = Style(color="black", bgcolor="bright_white")
    conf.txt_style = b_o_w


# Gets openai api key from config, envirnoment or file (aikey.txt)
if conf.openai_key != '':
    openai.api_key = conf.openai_key
elif "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]
else:
    openai.api_key = func.get_aikey()


# Sets variables
memory = []
the_world = ''
chapters = {}
definitions = ''
substitutions = ''



# Generates the first version of the world
console.print(Padding(l_p.starting_info, (1, 2, 2, 3)))

input_sum = func.add_inputs('Write your ideas below! If you want to skip to the menu, write "skip".')

if input_sum[0] != "skip":
    the_world = c_f.worldbuilding(input_sum)
    

# Main Loop
# Let's you select one of the worldbuilding options, then calls a 
# function to modify the description, save, load etc.

while True:
    console.print(Markdown(l_p.ask_options), style=conf.txt_style)
    options_1 = IntPrompt.ask()  
                      
    if options_1 == 1:
        memory.append(the_world)
        input_sum = func.add_inputs('Write your ideas!')
        the_world = c_f.worldbuilding(input_sum)


    elif int(options_1) > 1 and int(options_1) < 10:   

        if options_1 == 2:
            modified_world = c_f.inject_random(the_world)
            definitions = modified_world[0]
            substitutions = modified_world[2]
            modified_world = modified_world[1]

        elif options_1 == 3:
            concept_sum = func.add_inputs("What words, ideas, concepts should be introduced into the world?")
            modified_world = c_f.inject_non_random(the_world, concept_sum)

        elif options_1 == 4:
            modified_world = c_f.far_out_world(the_world)
            definitions = modified_world[0]
            substitutions = modified_world[2]
            modified_world = modified_world[1]

        elif options_1 == 5:
            modified_world = c_f.rebalance(the_world, input_sum)

        elif options_1 == 6:
            modified_world = c_f.decliche(the_world)

        elif options_1 == 7:
            modified_world = c_f.darken_world(the_world)

        elif options_1 == 8:
            modified_world = c_f.lighten_world(the_world)

        elif options_1 == 9:
            modified_world = c_f.defluff(the_world)


        if Confirm.ask('Do you want to keep the changes?') == True:
            memory.append(the_world)
            the_world = modified_world
        else:
            memory.append(modified_world)


    elif options_1 == 10:
        chapter_input = func.add_input("What is the chapter about?")
        new_content = c_f.generate_content(the_world, chapter_input)
        if Confirm.ask('Do you want to keep the generated content as a chapter?') == True:
            chapters[chapter_input] = new_content


    elif options_1 == 11:
        func.printout(the_world, chapters, definitions, substitutions)


    elif options_1 == 12:
        for x in range(len(memory)):
            console.print(Padding(f"MEMORY {len(memory) - x} \n {memory[x]}", (1, 2, 1, 3)))   # ok niby ale dziwne rzeczy się tu dzieją z kolorami


    elif options_1 == 13:
        if Confirm.ask('Should I clear definitions and substitutions') == True:
            definitions = ''
            substitutions = ''
        if Confirm.ask('Should I clear chapters, yes/no?') == True:
            chapters = {}
        if Confirm.ask('Should I clear memory, yes/no?') == True:
            memory = []


    elif options_1 == 14:
        rollback_world = func.rollback(memory)
        if rollback_world[0] == True:
            memory.append(the_world)
            the_world = rollback_world[1]


    elif options_1 == 15:
        saved_data = func.extract_data()
#        console.print(Padding(saved_data[0], {2, 2}), style=conf.txt_style)
        the_world = saved_data[0]
        chapters = json.loads(saved_data[1])
        definitions = saved_data[2]
        substitutions = saved_data[3]
        memory = json.loads(saved_data[4])
        input_sum = json.loads(saved_data[5])


    elif options_1 == 16:
        func.save_to_file(the_world, chapters, definitions, substitutions, memory, input_sum)

    
    elif options_1 == 17:
        console.print(Markdown(l_p.commands_info))
        
  


#TODO: 1, 2, 2, 3 czy nie powinno być 1, 2, 1, 3? Jak lepiej?
#TODO: memory print dobrze działa ale ma problem z kolorami w white theme

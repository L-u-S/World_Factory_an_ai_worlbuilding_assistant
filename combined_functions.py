import openai
import requests
import json
import os
from rich import print
from rich.console import Console
console = Console(width=50)

from config import Config

# VARIABLES
cnf = Config()

# WORLDBUILDING
worldbuilding_prompt = '''You are to outline information about a world that will be used in a tabletop roleplaying game.
Several users will provide information about the world they will want to play in. 
You are to generate an idea for a world. Following those rules:
- The ideas you write should not directly contradict any of the player ideas
- The world should be interesting and full of adventure
- The world can be of any type, not just fantasy, it can be a realistic modern setting, a horror, science-fiction or any other type of setting or combination thereof
- even if the players' ideas are divergent try to create a coherent world without partitioning it into wildly different countries/regions
'''

def worldbuilding_func(input_sum):
    messages = [{"role": "system", "content" : worldbuilding_prompt},
                {"role": "user", "content": '\n'.join(input_sum)}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response 

def worldbuilding(input_sum):
    the_world = worldbuilding_func(input_sum).choices[0].message.content
    print('\n\n\nThe first version:\n' + the_world + '\n------------------------')
    return the_world


# GENERATE CONTENT
generate_content_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying game and an input by a player who wants more information about some element of the world.

When responding use the following format:
Thought: think about how the player's input can be integrated into the world without changing it dramatically
Action: provide additional information about the element of the world the player wants to know more about
'''

def generate_content_func(the_world, chapter_input):
    messages = [{"role": "system", "content" : generate_content_prompt},
                {"role": "user", "content": the_world},
                {"role": "user", "content": chapter_input}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response 

def generate_content(the_world, chapter_input):
    new_content = generate_content_func(the_world, chapter_input).choices[0].message.content
    new_content = new_content.split('Action:')[1]
    print('\n\n\nThe new content:\n' + new_content + '\n------------------------')
    return new_content


# REBALANCE
rebalance_prompt = '''You will receive description of an imagined worlds that is to be used in tabletop roleplaying.
You will also receive players input with information about the world they will want to play in.   

When responding use the following format:
Thought: think if the imagined world will satisfy player's wishes, expressed in their input
Action: rewrite the description of the world in a way that will satisfy players' wishes, expressed in their input, while retaining ideas present in the original world description. The output should be at least as long as the original text. 
'''

def rebalance_func(the_world, input_sum):
    messages = [{"role": "system", "content" : rebalance_prompt},
                {"role": "user", "content": the_world},
                {"role": "user", "content": '\n'.join(input_sum)}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response         

def rebalance(the_world, input_sum):
    rebalanced = rebalance_func(the_world, input_sum).choices[0].message.content
    rebalanced = rebalanced.split('Action:')[1]
    print('\n\n\nThe new content:\n' + rebalanced + '\n------------------------')
    return rebalanced


# INJECT RANDOM
inject_random_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. You will also receive a list of random concepts. 
You will try to enrich the description of the world by utilizing the random concepts you received.

When responding use the following format:
Definitions: define the random concepts you received, each definition should be at most 15 words long
Thought: think about how to enrich the description of the word by using the concepts' definitions
Writing: write the new, enriched description of the world, it should be at least as long as the original description
Second thought: think if some of the random words in the new description are used in an uncommon, not proper or unintentionally humorous way
Action: provide suggestions what words might be substituted for the random words that are used in an uncommon, not proper or unintentionally humorous way
'''

aggressive_inject_random_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. You will also receive a list of random concepts. 
You will try to change the description of the world by utilizing the random concepts you received.

When responding use the following format:
Definitions: define the random concepts you received, each definition should be at most 15 words long
Thought: think about how to change the nature of the world taking inspiration from the concepts' definitions
Writing: write the new, description of the world, it should be at least as long as the original description
Second thought: think if some of the random words in the new description are used in an uncommon, not proper or unintentionally humorous way
Action: provide suggestions what words might be substituted for the random words that are used in an uncommon, not proper or unintentionally humorous way
'''

def inject_random_func(the_world, randomness):
    if input('\nShould we use aggresive injecting (more likely to change the natury of the world instead of just the description) yes or no?\n').lower() == "yes":
        custom_prompt = aggressive_inject_random_prompt
    else:
        custom_prompt = inject_random_prompt
    messages = [{"role": "system", "content" : custom_prompt},
                {"role": "user", "content": randomness},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response     

def inject_random(the_world):
    random_level = input(f"\nHow many random concepts should I inject?\n")
    if random_level.isnumeric() != True:
        print("\nI'm sorry but I need a number here.\n")
        inject_random(the_world)
    randomness = random_words(random_level)
    random_injected_world = inject_random_func(the_world, randomness).choices[0].message.content
    definitions = random_injected_world.split('Thought:')[0]
    print('\n\n\nThe modified version:\n' + 'First some definitions that may be needed to understand it all:\n' + definitions)
    random_injected_world_ideas = random_injected_world.split('Writing:')[1].split('Second thought:')[0]
    print(random_injected_world_ideas)
    substitutions = random_injected_world.split('Action:')[1]
    print('You might consider to:' + substitutions + '\n------------------------')
    return definitions, random_injected_world_ideas, substitutions 


# INJECT NON-RANDOM
def inject_non_random(the_world, concept_sum):
    concept_sum = ', '.join(concept_sum)
    non_random_injected_world = inject_random_func(the_world, concept_sum).choices[0].message.content
    non_random_injected_world = non_random_injected_world.split('Writing:')[1].split('Second thought:')[0]
    print(non_random_injected_world)
    return non_random_injected_world


# DECLICHE
aggressive_decliche_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world be be cliched and unoriginal.
You will list the cliches and stereotypes that are present and try to adjust the description of the world in order 
to avoid the cliches. 

When responding use the following format:
Find cliches: find and list all the cliches and stereotypes in the description
Thought: think about how to change the cliched content into a more original one,
Action: write a new. much more original, description of the world, it should be at least as long as the original description
'''

decliche_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world be be cliched and unoriginal.
You will list the cliches and stereotypes that are present and try to adjust the description of the world in order 
to avoid the cliches. 

When responding use the following format:
Find cliches: find and list all the cliches and stereotypes in the description
Thought: think about how to remove the cliches and stereotypes present while not changing the world in a dramatic manner
Action: write a new description of the world, it should be at least as long as the original description
'''

def decliche_func(the_world):
    if input('\nShould we use aggresive decliching (more likely to make the world dramatically \
                different and rather strange) yes/no?\n').lower() == "yes":
        custom_prompt = aggressive_decliche_prompt
    else:
        custom_prompt = decliche_prompt
    messages = [{"role": "system", "content" : custom_prompt},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response         

def decliche(the_world):
    decliched_world = decliche_func(the_world).choices[0].message.content
    decliched_world = decliched_world.split('Action:')[1]
    print('\n\n\nDecliched content:\n' + decliched_world + '\n------------------------')
    return decliched_world


# FAR OUT WORLD
far_out_world_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world be be cliched and unoriginal.
You will list the cliches and stereotypes that are present and try to adjust the description of the world in order 
to avoid the cliches. You will also receive a list of 8 random concepts.

When responding use the following format:
Find cliches: find and list all the cliches and stereotypes in the description
Definitions: define the random concepts you received, each definition should be at most 15 words long
Thought: think about how to reduce the stereotypes present in the description of the world by using the concepts' definitions
Writing: write the new, much weirder description of the world, it should be at least as long as the original description
Second thought: think if some of the random words in the new description are used in an uncommon, not proper or unintentionally humorous way
Action: provide suggestions what words might be substituted for the random words that are used in an uncommon, not proper or unintentionally humorous way
'''

def far_out_world_func(the_world, randomness):
    messages = [{"role": "system", "content" : far_out_world_prompt},
                {"role": "user", "content": randomness},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response     

def far_out_world(the_world):
    random_level = input(f"\nHow many random ideas should I inject?\n")
    if random_level.isnumeric() != True:
        print("\nI'm sorry but I need a number here.\n")
        far_out_world(the_world)
    randomness = random_words(random_level)
    odder_world = far_out_world_func(the_world, randomness).choices[0].message.content
    definitions = odder_world.split('Definitions:')[1].split('Thought:')[0]
    print('\n\n\nThe odder version:\n' + 'First some definitions that may be needed to understand it all:\n' + definitions)
    odder_world_ideas = odder_world.split('Writing:')[1].split('Second thought:')[0]
    print(odder_world_ideas)
    substitutions = odder_world.split('Action:')[1]
    print('You might consider to:' + substitutions + '\n------------------------')
    return definitions, odder_world_ideas, substitutions


# DEFLUFF
defluff_prompt = '''You will receive a text concerning an imagined world 
that is to be used in a tabletop roleplaying. You will calculate how many tokens the world description contains. 
You will divide the lenght in words by two and output a version of the text that has at least as many words as the result of the division.

When responding use the following format:
Measure: measure the world description lenght in tokens
Calculate: divide the lenght by two, the result is the target lenght of the output text
Action: output a shirtened world description using at least as many tokens as the result of the Calculate step
'''

def defluff_func(the_world):
    messages = [{"role": "system", "content" : defluff_prompt},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response         

def defluff(the_world):
    defluffed_world = defluff_func(the_world).choices[0].message.content
    defluffed_world = defluffed_world.split('Action: ')[1]
    print('\n\n\nDefluffed description:\n' + defluffed_world)
    return defluffed_world
    


# DARKEN WORLD
darkened_world_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world will probably lack some elements conductive of conflict, 
and some of the darker themes present in fiction will not be adressed.

When responding use the following format:
Thought: think about how can you add more danger, more mature elements and more edgelord antics to the world, without changing the world in a dramatic manner 
Action: rewrite the description in a way that will be significantly more dangerous, more mature and suffused with edgelord antics, without changing the world in a dramatic manner. The new description should be at least as long as the original description 
'''

def darken_world_func(the_world):
    messages = [{"role": "system", "content" : darkened_world_prompt},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response         

def darken_world(the_world):
    darker_world = darken_world_func(the_world).choices[0].message.content
    darker_world = darker_world.split('Action:')[1]
    print('\n\n\nThe darker version:\n' + darker_world + '\n------------------------')
    return darker_world


# LIGHTEN WORLD

lightened_world_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world will probably be grim, dark and devoid of hope.

When responding use the following format:
Thought: think about how can you address more values like love, honor, friendship and heroism in the description of the world without changing the world in a dramatic manner 
Action: rewrite the description in a way that will be significantly more light-hearted, and conductive to adress values such as love, honor, friendship and heroism, without changing the world in a dramatic manner. The new description should be at least as long as the original description 
'''

def lighten_world_func(the_world):
    messages = [{"role": "system", "content" : lightened_world_prompt},
                {"role": "user", "content": the_world}]
    response = openai.ChatCompletion.create(
        model=cnf.chat_models[cnf.model],
        messages=messages,
        temperature = 1)
    return response         

def lighten_world(the_world):
    lighter_world = lighten_world_func(the_world).choices[0].message.content
    lighter_world = lighter_world.split('Action:')[1]
    print('\n\n\nThe lighter version:\n' + lighter_world + '\n------------------------')
    return lighter_world


# FUNCTIONS
def add_input(text):
    added_input = input(f'''\n{text}\n''') 
    return added_input


def add_inputs(text):
    inputs = []
    print(f'''\n{text} If that's all, just write: "ok":\n''')
    while True:
        idea_input = input()
        if idea_input.lower() == "ok":
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
        print('\n\n' + the_world + '\n------------------------')
    except: 
        pass
    
    try:
        for key, value in chapters.items():
            print(f'\n\n {key.upper()} \n\n {value}')
    except:
        pass
    
    try:
        print(f'\n\n {definitions} \n\n {substitutions}')
    except:
        pass    


def rollback(memory):
    world_number = input('\n\nHow far should I roll back?\n')
    if world_number.isnumeric() != True:
        print("\nI'm sorry but I need a number here.\n")
        rollback(memory)
    world_number = -(int(world_number))
    try:
        print('\n\n' + memory[world_number] + '\n------------------------')
        if input('\nDo you want to make this world the primary one, yes/no?\n').lower() == "yes":
            return (True, memory[world_number])
        else:
            return (False)
    except:
        print('\n\nSorry, no such world! Try again.\n')
        return (False)


def extract_data():
    file_number = input('What number does the file have (e.g. my_world_3.txt is number 3)?')
    if file_number.isnumeric() != True:
        print("\nI'm sorry but I need a number here.\n")
        extract_data()
    app_path = os.getcwd()
    file_path = f"{app_path}\saved worlds\my_world_{file_number}.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            saved_data = file.read()
            the_world = saved_data.split('------------------------')[0]
            chapters = saved_data.split('CHAPTERS: ')[1].split('------------------------')[0]
            definitions = saved_data.split('DEFINITIONS: ')[1].split('------------------------')[0]
            substitutions = saved_data.split('SUBSTITUTIONS: ')[1].split('------------------------')[0]
            memory = saved_data.split('MEMORY: ')[1].split('------------------------')[0]
            input_sum = saved_data.split('INPUT SUM: ')[1].split('------------------------')[0]
            return the_world[8:], chapters, definitions, substitutions, memory, input_sum



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
    print(f"\n\nSaved as: {file_path}\n")

def get_aikey():
    app_path = os.getcwd()
    file_path = f"{app_path}/aikey.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            aikey = str(file.read())
            return aikey
    else:
        aikey = input("\n\nI'm sorry but I can't find the openai api key. Please provide it\
                      either by placing it in config.openai_key or in aikey.txt file.\n\n")

# NOT USED
def split_description(description, split_word, index):
    try:
        output = description.split(split_word)[index]
        return output
    except:
        print("\n\n Something went wrong! Returning whole content. If it's bad don't save it!\n")
        return description


#TODO: Nadal jest problem z shorten wyrzucającym 114 tokens etc i trochę za bardzo skraca chyba
# ostatecznie

# TODO: git dependencies


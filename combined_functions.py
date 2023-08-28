import openai

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.prompt import IntPrompt
from rich.prompt import Confirm
from rich.padding import Padding
from rich.style import Style


from config import Config
import functions as func


'''This file contains all the functions that send user commands, inputs etc to ChatGTP.
    Most functions have three elements: chat prompt, function that sends the 
    commands to ai and a function that is called from the main app, sends info to the ai-facing 
    function and then works on the output (cutting out the chain-of-thought elements usually)  
    so it can be printed out to the user
    
    So if user chooses 'Rebalance' option in the terminal app, {rebalance} function is called, 
    it sends infomation to {rebalance_func} that uses {rebalance_prompt} in order to instruct 
    ChatGTP how to modify the description of the world. {rebalance_func} sends ai response back to 
    {rebalance} which cuts it, prints it and returns it to the main app, the main app will
    then ask if the output is ok. If it is, the output becomes a "primary" world and old text is
    saved to in-app memory (which is basically a list of strings)'''



# SETUP
conf = Config()
console = Console(width=100)
red_style = Style(color="red", bold=True)



# WORLDBUILDING
# This is the main function, it creates the outline of the world.
# it does not use chain-of-thought so the output can be printed out as is.


worldbuilding_prompt = '''You are to outline information about a world that will be used in a tabletop roleplaying game.
Several users will provide information about the world they will want to play in. 
You are to generate an idea for a world. Following those rules:
- The ideas you write should not directly contradict any of the player ideas
- The world should be interesting and full of adventure
- The world can be of any type, not just fantasy, it can be a realistic modern setting, a horror, science-fiction or any other type of setting or combination thereof
- Even if the players' ideas are divergent try to create a coherent world without partitioning it into wildly different countries/regions
'''

def worldbuilding_func(input_sum):
    """
    worldbuilding_func sends user's ideas to LLM, returns its output.

    :param input_sum: list of strings with user input (user's ideas about the world)
    :return: llm response
    """ 
    messages = [{"role": "system", "content" : worldbuilding_prompt},
                {"role": "user", "content": '\n'.join(input_sum)}]
    console.print(Padding('[blink]Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response 

def worldbuilding(input_sum):
    """
    worldbuilding sends user's ideas to worldbuilding_func, gets back LLM output, takes text
    from the response, prints it, returns it to the main app.

    :param input_sum: list of strings with user input (user's ideas about the world)
    :return: text from llm response as string
    """ 
    the_world = worldbuilding_func(input_sum).choices[0].message.content
    console.print(Padding('Primary world description:\n' + the_world, (1, 2, 1, 3)))
    return the_world


# GENERATE CONTENT
# This function creates chapters. Chapters are kept separately from the description of the world
# and are not mutated alongside it.

generate_content_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying game and an input by a player who wants more information about some element of the world.

When responding use the following format:
Thought: think about how the player's input can be integrated into the world without changing it dramatically
Action: provide additional information about the element of the world the player wants to know more about
'''

def generate_content_func(the_world, chapter_input):
    """
    generate_content_func sends the world description and player info the subject of the new
    chapter to LLM, returns its output.

    :param the_world: the description of the world as a string
    :param chapter_input: a string with user's input (the subject of the chapter)
    :return: llm response
    """ 
    messages = [{"role": "system", "content" : generate_content_prompt},
                {"role": "user", "content": the_world},
                {"role": "user", "content": chapter_input}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response 

def generate_content(the_world, chapter_input):
    """
    generate_content sends the world description and player info about what the new chapter
    should be about to generate_content_func, gets back LLM output, takes text from the
    response, splits it to get rid of chain of thought elements, prints it, returns it to the
    main app.

    :param the_world: the description of the world as a string
    :param chapter_input: a string with user's input (the subject of the chapter)
    :return:  text from llm response as string
    """ 
    new_content = generate_content_func(the_world, chapter_input).choices[0].message.content
    new_content = new_content.split('Action:')[1]
    console.print(Padding('The new content:\n' + new_content, (1, 2, 1, 3)))
    return new_content


# REBALANCE
# This function reinjects original ideas of the user into a mutated world.
# Its aim is to keep the changes introduced during the mutation process while also making the
# world more in-line with the original vision.

rebalance_prompt = '''You will receive description of an imagined worlds that is to be used in tabletop roleplaying.
You will also receive players input with information about the world they will want to play in.   

When responding use the following format:
Thought: think if the imagined world will satisfy player's wishes, expressed in their input
Action: rewrite the description of the world in a way that will satisfy players' wishes, expressed in their input, while retaining ideas present in the original world description. The output should be at least as long as the original text. 
'''

def rebalance_func(the_world, input_sum):
    """
    rebalance_func sends the world description and original user's ideas to LLM, returns its output.

    :param the_world: the description of the world as a string
    :param input_sum: a list of strings with user input (user's ideas about the world)
    :return: llm response
    """
    messages = [{"role": "system", "content" : rebalance_prompt},
                {"role": "user", "content": the_world},
                {"role": "user", "content": '\n'.join(input_sum)}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response         

def rebalance(the_world, input_sum):
    """
    rebalance sends the world description and original user's ideas to rebalance_func LLM,
    gets back LLM output, takes text from the response, splits it to get rid of chain of thought
    elements, prints it, returns it to the main app.

    :param the_world: the description of the world as a string
    :param input_sum: a list of strings with user input (user's ideas about the world)
    :return: text from llm response as string
    """
    rebalanced = rebalance_func(the_world, input_sum).choices[0].message.content
    rebalanced = rebalanced.split('Action:')[1]
    console.print(Padding('The new content:\n' + rebalanced, (1, 2, 1, 3)))
    return rebalanced


# INJECT RANDOM
# This injects random words. It uses https://random-word-api as a source of the words.
# The output text must be split several times as it contains definitions of the words,
# and suggestions for their substitutions if they sound too strange. Definitions and substitions
# are also returned to the main app and saved.
# There are two prompts here: regular and aggressive. Aggressive prompt "allows" the ai to
# change the nature of the world more dramatically while injecting the words.

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
    """
    inject_random_func sends the world description and several random words to LLM, returns its
    output. Before sending, it asks if "aggressive injecting" should be used. It chooses the
    prompt (either inject_random_prompt or aggressive_inject_random_prompt) based on the response.

    :param the_world: the description of the world as a string
    :param randomness: string with words separated by commas (output of
    random-word-api.herokuapp.com)
    :return: llm response
    """
    if Confirm.ask('\nShould we use aggresive injecting (more likely to change the natury of the world instead of just the description)?\n') == True:
        custom_prompt = aggressive_inject_random_prompt
    else:
        custom_prompt = inject_random_prompt
    messages = [{"role": "system", "content" : custom_prompt},
                {"role": "user", "content": randomness},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response     

def inject_random(the_world):
    """
    inject_random asks for a number of random objects to inject and uses functions.random_words
    to  get them from random-word-api.herokuapp.com. Then it sends the world description and random
    words to inject_random_func, gets back LLM output, takes text from the response. The text is
    split in order to use several chain-of-thought elements such as word definitions and possible
    subsitutions. ALl those elements are printed and returned to the main app.

    :param the_world: the description of the world as a string
    :return: texts from llm response as strings
    """
    console.print(Padding('How many random concepts should I inject?', (1, 2, 1, 3)))
    random_level = IntPrompt.ask()
    randomness = func.random_words(random_level)
    random_injected_world = inject_random_func(the_world, randomness).choices[0].message.content
    definitions = random_injected_world.split('Thought:')[0]
    console.print(Padding('The modified version:\n' + 'First some definitions that may be needed to understand it all:\n' + definitions, (1, 3)), style=conf.txt_style)
    random_injected_world_ideas = random_injected_world.split('Writing:')[1].split('Second thought:')[0]
    console.print(Padding(random_injected_world_ideas, (1, 2, 1, 3)))
    substitutions = random_injected_world.split('Action:')[1]
    console.print(Padding('You might consider to:\n' + substitutions, (1, 3)), style=conf.txt_style)
    return definitions, random_injected_world_ideas, substitutions 


# INJECT NON-RANDOM
# This function uses the inject_random_func and prompts, but the words injected are defined by
# the user instead of downloaded.

def inject_non_random(the_world, concept_sum):
    """
    inject_non_random asks user to input a number of concepts and uses sends them, along with the
    world description to inject_random_func, gets back LLM output, takes text from the response,
    splits it in order to get rid of chain-of-thought elements, prints it and returns to the main
    app.

    :param the_world: the description of the world as a string
    :return: text from llm response as string
    """
    concept_sum = ', '.join(concept_sum)
    non_random_injected_world = inject_random_func(the_world, concept_sum).choices[0].message.content
    non_random_injected_world = non_random_injected_world.split('Writing:')[1].split('Second thought:')[0]
    console.print(Padding('Modified version:\n' + non_random_injected_world, (1, 2, 1, 3)))
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
    """
    decliche_func sends the world description to LLM and returns its output. Before sending,
    it asks if "aggressive decliche" should be used. It chooses the prompt (either
    decliche_prompt or aggressive_decliche_prompt) based on the response.

    :param the_world: the description of the world as a string
    :return: llm response
    """
    if Confirm.ask('\nShould we use aggresive decliching (more likely to make the world dramatically \
                different and rather strange)?') == True:
        custom_prompt = aggressive_decliche_prompt
    else:
        custom_prompt = decliche_prompt
    messages = [{"role": "system", "content" : custom_prompt},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response         

def decliche(the_world):
    """
    decliche sends the world description to decliche_func, gets back LLM output, takes text from
    the response,splits it in order to get rid of chain-of-thought elements, prints it and
    returns to the main app.

    :param the_world: the description of the world as a string
    :return: text from llm response as string
    """
    decliched_world = decliche_func(the_world).choices[0].message.content
    decliched_world = decliched_world.split('Action:')[1]
    console.print(Padding('Decliched content:\n' + decliched_world, (1, 2, 1, 3)))
    return decliched_world


# FAR OUT WORLD
# This function uses aggresive decliching alongside aggresive inject random 
# The effect is a totally changed description, often diametrically opposite 
# to the original vision. 

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
    """
    far_out_world_func sends the world description and several random words to LLM, returns its
    output.

    :param the_world: the description of the world as a string
    :param randomness: string with words separated by commas (output of
    random-word-api.herokuapp.com)
    :return: llm response
    """
    messages = [{"role": "system", "content" : far_out_world_prompt},
                {"role": "user", "content": randomness},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response     

def far_out_world(the_world):
    """
    far_out_world works almost identcally to inject_random: it asks for a number of random
    objects to inject and uses functions.random_words to  get the words from
    random-word-api.herokuapp.com. Then it sends the world description and random
    words to far_out_world_func, gets back LLM output, takes text from the response. The text is
    split in order to use several chain-of-thought elements such as word definitions and possible
    subsitutions. ALl those elements are printed and returned to the main app.

    :param the_world: the description of the world as a string
    :return: texts from llm response as strings
    """
    console.print(Padding('How many random concepts should I inject?', (1, 2, 1, 3)))
    random_level = IntPrompt.ask()
    randomness = func.random_words(random_level)
    odder_world = far_out_world_func(the_world, randomness).choices[0].message.content
    definitions = odder_world.split('Definitions:')[1].split('Thought:')[0]
    console.print(Padding('The odder version:\n' + 'First some definitions that may be needed to understand it all:\n' + definitions, (1, 3)))
    odder_world_ideas = odder_world.split('Writing:')[1].split('Second thought:')[0]
    console.print(Padding(odder_world_ideas, (1, 2, 1, 3)))
    substitutions = odder_world.split('Action:')[1]
    console.print(Padding('You might consider to:' + substitutions, (1, 2, 1, 3)))
    return definitions, odder_world_ideas, substitutions


# DEFLUFF
# This aims to shorten the world description without collapsing it into 
# a two sentence summarization. The Chat does not actually follow the prompt
# in a precise manner, but it usually outputs what it should (I tested many,
# many versions of it and most of them were even more defective).  

defluff_prompt = '''You will receive a text concerning an imagined world 
that is to be used in a tabletop role-playing. You will calculate how many tokens the world description contains. 
You will divide the length in words by two and output a version of the text that has at least as many words as the result of the division.

When responding use the following format:
Measure: measure the world description length in tokens
Calculate: divide the length by two, the result is the target length of the output text
Action: output a shortened world description using at least as many tokens as the result of the Calculate step
'''

def defluff_func(the_world):
    """
    defluff_func sends the world description to LLM and returns its output.

    :param the_world: the description of the world as a string
    :return: llm response
    """
    messages = [{"role": "system", "content" : defluff_prompt},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response         

def defluff(the_world):
    """
    defluff sends the world description to defluff_func, gets back LLM output, takes text from
    the response,splits it in order to get rid of chain-of-thought elements, prints it and
    returns to the main app. It also uses a somewhat ugly fix described below.

    :param the_world: the description of the world as a string
    :return: text from llm response as string
    """
    defluffed_world = defluff_func(the_world).choices[0].message.content
    defluffed_world = defluffed_world.split('Action: ')[1]
    
    # a fix for a recurring problem of ai spitting out parts of the
    # system prompt in the response 
    if 'tokens.' in defluffed_world:
        defluffed_world = defluffed_world.split('tokens.')[1]
    elif 'tokens' in defluffed_world:
        defluffed_world = defluffed_world.split('tokens')[1]
        
    console.print(Padding('Defluffed description:\n' + defluffed_world, (1, 2, 1, 3)))
    return defluffed_world
    


# DARKEN WORLD
# This makes the world grimdark.

darkened_world_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world will probably lack some elements conductive of conflict, 
and some of the darker themes present in fiction will not be adressed.

When responding use the following format:
Thought: think about how can you add more danger, more mature elements and more edgelord antics to the world, without changing the world in a dramatic manner 
Action: rewrite the description in a way that will be significantly more dangerous, more mature and suffused with edgelord antics, without changing the world in a dramatic manner. The new description should be at least as long as the original description 
'''

def darken_world_func(the_world):
    """
    darken_world_func sends the world description to LLM and returns its output.

    :param the_world: the description of the world as a string
    :return: llm response
    """
    messages = [{"role": "system", "content" : darkened_world_prompt},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response         

def darken_world(the_world):
    """
    darken_world sends the world description to darken_world_func, gets back LLM output,
    takes text from the response,splits it in order to get rid of chain-of-thought elements,
    prints it and returns to the main app.

    :param the_world: the description of the world as a string
    :return: text from llm response as string
    """
    darker_world = darken_world_func(the_world).choices[0].message.content
    darker_world = darker_world.split('Action:')[1]
    console.print(Padding('The darker version:\n' + darker_world, (1, 2, 1, 3)))
    return darker_world


# LIGHTEN WORLD
# This makes the word less grimdark.

lightened_world_prompt = '''You will receive an information about an imagined world 
that is to be used in a tabletop roleplaying. This world will probably be grim, dark and devoid of hope.

When responding use the following format:
Thought: think about how can you address more values like love, honor, friendship and heroism in the description of the world without changing the world in a dramatic manner 
Action: rewrite the description in a way that will be significantly more light-hearted, and conductive to adress values such as love, honor, friendship and heroism, without changing the world in a dramatic manner. The new description should be at least as long as the original description 
'''

def lighten_world_func(the_world):
    """
    lighten_world_func sends the world description to LLM and returns its output.

    :param the_world: the description of the world as a string
    :return: llm response
    """
    messages = [{"role": "system", "content" : lightened_world_prompt},
                {"role": "user", "content": the_world}]
    console.print(Padding('Processing, might take a while', (1, 3)), style=red_style)
    response = openai.ChatCompletion.create(
        model=conf.chat_models[conf.model],
        messages=messages,
        temperature = 1)
    return response         

def lighten_world(the_world):
    """
    lighten_world sends the world description to lighten_world_func, gets back LLM output,
    takes text from the response,splits it in order to get rid of chain-of-thought elements,
    prints it and returns to the main app.

    :param the_world: the description of the world as a string
    :return: text from llm response as string
    """
    lighter_world = lighten_world_func(the_world).choices[0].message.content
    lighter_world = lighter_world.split('Action:')[1]
    console.print(Padding('The lighter version:\n' + lighter_world, (1, 2, 1, 3)))
    return lighter_world


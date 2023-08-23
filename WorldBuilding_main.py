import openai
import json

from rich import print
from rich.console import Console
from rich.markdown import Markdown

console = Console(width=100)

import combined_functions as c_f
from config import Config
import loose_prompts as l_p

# VARIABLES
cfg = Config()

if cfg.openai_key == '':
    openai.api_key = c_f.get_aikey()
else:
    openai.api_key = cfg.openai_key

memory = []
chapters = {}
definitions = ''
substitutions = ''


# GENERATE THE WORLD
console.print(l_p.ai_starting_info)
console.print(Markdown(l_p.ai_starting_table_info))

input_sum = c_f.add_inputs('Write your ideas! If you want to skip to the menu, write "skip".')


if input_sum[0] != "skip":
    the_world = c_f.worldbuilding(input_sum)
    memory.append(the_world)


# MAIN LOOP
while True:
    options_1 = input("\n------------------------\nWhat do you want to do now?\
                        \n1. Generate a new world\
                        \n2. Inject random concepts\
                        \n3. Inject non-random concepts\
                        \n4. Super-weirdness (aggresive decliche + inject random)\
                        \n5. Rebalance world\
                        \n6. Cliche reduction\
                        \n7. Darken the world\
                        \n8. Brighten the world\
                        \n------------------------\
                        \n9. Shorten the text\
                        \n10. Generate a chapter\
                        \n------------------------\
                        \n11. See what you have\
                        \n12. Display memory (previous versions of your world)\
                        \n13. Clear data\
                        \n14. Load world from memory\
                        \n15. Load world from file\
                        \n16. Save the world!\
                        \n------------------------\n")
                        
    if options_1.isdigit():
        if options_1 == "1":
            memory.append(the_world)
            input_sum = c_f.add_inputs('Write your ideas!')
            the_world = c_f.worldbuilding(input_sum)


        elif int(options_1) > 1 and int(options_1) < 10:   # to musi być sanitized do samych numbers

            if options_1 == "2":
                modified_world = c_f.inject_random(the_world)
                definitions = modified_world[0]
                substitutions = modified_world[2]
                modified_world = modified_world[1]

            elif options_1 == "3":
                concept_sum = c_f.add_inputs("What words, ideas, concepts should be introduced into the world?")
                modified_world = c_f.inject_non_random(the_world, concept_sum)

            elif options_1 == "4":
                modified_world = c_f.far_out_world(the_world)
                definitions = modified_world[0]
                substitutions = modified_world[2]
                modified_world = modified_world[1]

            elif options_1 == "5":
                modified_world = c_f.rebalance(the_world, input_sum)

            elif options_1 == "6":
                modified_world = c_f.decliche(the_world)

            elif options_1 == "7":
                modified_world = c_f.darken_world(the_world)

            elif options_1 == "8":
                modified_world = c_f.lighten_world(the_world)

            elif options_1 == "9":
                modified_world = c_f.defluff(the_world)


            if input('\nDo you want to keep the changes, yes or no?\n').lower() == "yes":
                memory.append(the_world)
                the_world = modified_world

            else:
                memory.append(modified_world)


        elif options_1 == "10":
            chapter_input = c_f.add_input("What is the chapter about?")
            new_content = c_f.generate_content(the_world, chapter_input)
            if input('\nDo you want to keep the additional information as and additional chapter, yes or no?\n').lower() == "yes":
                chapters[chapter_input] = new_content


        elif options_1 == "11":
            c_f.printout(the_world, chapters, definitions, substitutions)


        elif options_1 == "12":
            console.print('\n\n' + '\n------------------------\n\n'.join(memory) + '\n------------------------\n')


        elif options_1 == "13":
            if input('\nShould I clear definitions and substitutions, yes/no?\n\n') == "yes":
                definitions = ''
                substitutions = ''
            if input('\nShould I clear chapters, yes/no?\n\n') == "yes":
                chapters = {}
            if input('\nShould I clear memory, yes/no?\n\n') == "yes":
                memory = []


        elif options_1 == "14":
            rollback_world = c_f.rollback(memory)
            if rollback_world[0] == True:
                memory.append(the_world)
                the_world = rollback_world[1]


        elif options_1 == "15":
            saved_data = c_f.extract_data()
            console.print(saved_data)
            the_world = saved_data[0]
            chapters = json.loads(saved_data[1])
            definitions = saved_data[2]
            substitutions = saved_data[3]
            memory = json.loads(saved_data[4])
            input_sum = json.loads(saved_data[5])


        elif options_1 == "16":
            c_f.save_to_file(the_world, chapters, definitions, substitutions, memory, input_sum)
    else:
        console.print('Something went wrong. Maybe try selecting some of the options?')
    
   




# This is information for users, most of it in markdown.

starting_info = '''Hello! Welcome to the worldbuilding module. My purpose is to assist you in creating a description of an imaginary world. 
First I would like you to give me with some ideas.'''

commands_info = '''
|Actions|What do they do?|
|---|---|
|1. Generate a new world|Discard your current progress and begin afresh.|
|&nbsp;|&nbsp;|
|2. Inject random concepts|Several random words will be interpreted by the AI and incorporated into the world's description. You can decide how many random words to inject and whether the injection should be aggressive. A non-aggressive injection will make minor changes to the world, while an aggressive one might alter the direction of the world based on the random concepts.|
|&nbsp;|&nbsp;|
|3. Inject non-random concepts| Similar to the previous option, but instead of random words, you input the specific words/concepts to be used.
|&nbsp;|&nbsp;|
|4. Super-weirdness| Aggresive decliche + inject random. This option will make the world quite strange and almost unrecognizable, but it has the potential to generate unique outcomes.
|&nbsp;|&nbsp;|
|5. Rebalance world| This option will keep the changes made so far while attempting to reintroduce your original ideas to the world.
|&nbsp;|&nbsp;|
|6. Decliche| This option will try to make the world less stereotypical. There are two modes available: aggressive mode, which can significantly alter the world to avoid what the AI perceives as cliches and stereotypes, and non-aggresive mode, which will only soften some of the more stereotypical elements.
|&nbsp;|&nbsp;|
|7. Darken the world| Makes the world more grimdark.
|&nbsp;|&nbsp;|
|8. Brighten the world| Makes the world sunnier and more heroic.
|&nbsp;|&nbsp;|
|9. Shorten the text| Makes the description shorter.
|&nbsp;|&nbsp;|
|10. Generate a chapter| Creates additional detailed text describing an element in the world, such as a group, race, place, or conflict. This text will be independent of the general description and will not be altered alongside it. It is recommended to generate chapters after finalizing the description.
|&nbsp;|&nbsp;|
|11. See what you have| Displays the current state of the world.
|&nbsp;|&nbsp;|
|12. Display memory| Displays all the versions of the world that have been created in the current session.
|&nbsp;|&nbsp;|
|13. Clear data| Deletes current session data, including chapters, word definitions, and memory.
|&nbsp;|&nbsp;|
|14. Load world from memory| Replaces the current world description with a version from memory.
|&nbsp;|&nbsp;|
|15. Load world from file| Imports a saved world description from a file. The files are in the app folder/data and they are numbered. The app will ask you about the number of the file you want to load.
|&nbsp;|&nbsp;|
|16. Save the world!| Saves the world description, along with chapters, definitions, substitutions, and memory, to a text file in app folder/data.
|&nbsp;|&nbsp;|
|17. HELP!|It helps.
'''

ask_options = """
&nbsp;
# What do you want to do?
|#|Primary actions|#|Other actions|#|Save & load
|--|--|--|--|--|--
|1|Generate a new world|9|Shorten the text|11|See what you have
|2|Inject random concepts|10|Generate a chapter|12|Display memory
|3|Inject non-random concepts|&nbsp;|&nbsp;|13|Clear data
|4|Super-weirdness|&nbsp;|&nbsp;|14|Load world from memory
|5|Rebalance world|&nbsp;|&nbsp;|15|Load world from file
|6|Decliche|&nbsp;|&nbsp;|16|Save the world!
|7|Darken the world|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|8|Brighten the world|&nbsp;|&nbsp;|17|HELP!|

"""

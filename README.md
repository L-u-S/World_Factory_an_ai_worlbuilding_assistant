# AI Create Worlds

---
This is a small project aiming to coax ChatGTP into being more creative when describing imagined 
worlds.


## What is the idea?

---
The original aim of this project was to build a framework for cooperative worldbuilding, where 
several users interact with ChatGTP and create a shared world that can be used in tabletop rpgs.  

The main problem was that the AI generated content is just not very ... good. AIs are, by nature 
and design, trained to be consistent rather than original / creative.

In this project I tried to use several strategies to make the worlds ChatGTP can dream about, 
more interesting.
 


## How does it work?

---
First, the user writes about his or her ideas about the world, then ChatGTP generates the first 
draft of the world's description. It looks like this:

&nbsp;

![screen_1.jpg](img%2Fscreen_1.jpg)

&nbsp;

Then the outline can be "mutated" using several commands:

&nbsp;

![screen_2.jpg](img%2Fscreen_2.jpg)

&nbsp;
&nbsp;

The main actions that can be used are based around "injecting" concepts into the description.

Those concepts can be random (random words are downloaded from https://random-word-api.herokuapp.
com/
and then ChatGTP is instructed to rewrite the description of the world using them as inspiration) 
or defined by the user. 


The effects are usually quite wild and unpredictable, so there are several other commands that 
give the user some control over the world's description.

&nbsp;

All the commands are described at the end of this readme. The descriptions can also be read 
in-app by using the "HELP!" command. 

&nbsp;

The effects can look like this (this is super-weirdness command in action):

&nbsp;

![screen_3.jpg](img%2Fscreen_3.jpg)

&nbsp;

As you can see it can get quite odd, but at least, from time to time, some 
interesting ideas can be (automatically) generated.  


## The technical stuff

---
There is not much of it.

The whole app is run in terminal, using Rich to prettify the results. 

All the ai-facing functions are in the combined_functions.py - most of the work on the app was 
spent on getting the prompts (kind of) right. 

This app needs an openai api key. It can be set as an environmental variable, placed in config.py 
as self.openai_key or put into aikey.txt file that has to be placed in the app folder.

I placed an exe version of the file on github, this version needs aikey.txt in order to work. 


## The commands

---
&nbsp;

|Actions|What do they do?|
|---|---|
|1. Generate a new world|Discard your current progress and begin afresh.|
|2. Inject random concepts|Several random words will be interpreted by the AI and incorporated into the world's description. You can decide how many random words to inject and whether the injection should be aggressive. A non-aggressive injection will make minor changes to the world, while an aggressive one might alter the direction of the world based on the random concepts.|
|3. Inject non-random concepts| Similar to the previous option, but instead of random words, you input the specific words/concepts to be used.
|4. Super-weirdness| Aggresive decliche + inject random. This option will make the world quite strange and almost unrecognizable, but it has the potential to generate unique outcomes.
|5. Rebalance world| This option will keep the changes made so far while attempting to reintroduce your original ideas to the world.
|6. Decliche| This option will try to make the world less stereotypical. There are two modes available: aggressive mode, which can significantly alter the world to avoid what the AI perceives as cliches and stereotypes, and non-aggresive mode, which will only soften some of the more stereotypical elements.
|7. Darken the world| Makes the world more grimdark.
|8. Brighten the world| Makes the world sunnier and more heroic.
|9. Shorten the text| Makes the description shorter.
|10. Generate a chapter| Creates additional detailed text describing an element in the world, such as a group, race, place, or conflict. This text will be independent of the general description and will not be altered alongside it. It is recommended to generate chapters after finalizing the description.
|11. See what you have| Displays the current state of the world.
|12. Display memory| Displays all the versions of the world that have been created in the current session.
|13. Clear data| Deletes current session data, including chapters, word definitions, and memory.
|14. Load world from memory| Replaces the current world description with a version from memory.
|15. Load world from file| Imports a saved world description from a file.
|16. Save the world!| Saves the world description, along with chapters, definitions, substitutions, and memory, to a text file on your computer.
|17. HELP!|Helps.


## TODO:

---
I think there are several more things to do:

- General debugging and prettyfing
- Adding picture generation
- Adding option for mutating chapters in line with the general description
- Trying the same on Llama-based LLMs (maybe they are more creative?)
- Can we actually induce LLMs to hallucinate more? It could help.


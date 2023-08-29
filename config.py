from rich.style import Style

class Config():
    def __init__(self):

# This is where you can put an openai_key and switch openai models, the 
# app default is 3.5 turbo 
        # AI PARAMETERS
        self.openai_key = ''
        self.chat_models = ["gpt-3.5-turbo-0613", "gpt-4-0613"]
        self.model = 0

        # UI PARAMETERS
        self.black_on_white_style = True
        self.style_types = {
        'default' : Style(),
        'bow' : Style(color="black", bgcolor="bright_white")
        }


# This starts up a black-on_white terminal style, unfortunately at this 
# moment there is a slight problem with rendering in Rich that will make 
# some symbols printed on a wrong background. 

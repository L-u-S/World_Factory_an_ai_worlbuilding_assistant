from rich.style import Style

class Config():
    def __init__(self):

        # AI PARAMETERS
        self.openai_key = ''
        self.chat_models = ["gpt-3.5-turbo-0613", "gpt-4-0613"]
        self.model = 0
        
        # UI PARAMETERS
        self.black_on_white_style = False
        self.txt_style = Style()

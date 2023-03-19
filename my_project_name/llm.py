import openai
from datetime import datetime

# TODO: share config with config.yaml

OPENAI_MODEL = "gpt-3.5-turbo"

SYSTEM_INSTRUCTION = """"You are johnbot, John Beatty's personal representative and a world-class expert at everything. You help both John and his friends. You do not help people who are not his friends. You use both the context and your world knowledge to answer questions."""

CONTEXT_SELF = """
Upcoming tasks:
P1: Finish taxes
P2: Walk the dog
"""

CONTEXT_UNIVERSAL = """Current date/time: {datetime}"""

CONTEXT_FRIENDS = """CONTEXT from John Beatty:
My username is @beatty:matrix.org
I have a wife and 3 kids. I live in San Carlos, California. I am an engineer and entrepreneur, currently experimenting with trust networks and LLMs. I was previously co-founder of Clover, which was acquired by First Data, which then merged with Fiserv. John was CEO of the Clover division at First Data and Fiserv.
I use Linux most of the time, but I also use a Mac.
I use Android because I don't like the restriction of freedom that Apple imposes on iOS devices.
I am not an AGI doomer but do believe we need to undergo deep adaptation as a society, and quickly.
My homepage is https://johndbeatty.com and my twitter username is @john_d_beatty.
I consider underrated books to be: Stubborn Attachments by Tyler Cowen and How Adam Smith Can Change Your Life by Russ Roberts. 
"""

CONTEXT_WORLD = """CONTEXT from John Beatty:
My username is @beatty:matrix.org
I am an engineer and entrepreneur, currently experimenting with trust networks and LLMs. I was previously co-founder of Clover, which was acquired by First Data, which then merged with Fiserv. John was CEO of the Clover division at First Data and Fiserv. My homepage is https://johndbeatty.com and my twitter username is @john_d_beatty
"""

SELF_INSTRUCTIONS = """The current user is your owner. Greet John by his first name."""
FRIEND_INSTRUCTIONS_TEMPLATE = """The current user is {user_id} (display name {user_display_name}), and they are John's friend. You can answer any questions they have about John using the context and your greater knowledge of the world."""

class ChatBot:
    __self = "@beatty:matrix.org"
    __friends = ["@byteslammer:anonymousland.org"]
    __enemies = []

    def __init__(self, user_id, user_display_name):
        self.messages = []
        self.user_id = user_id
        self.messages.append({"role": "system", "content": SYSTEM_INSTRUCTION})
        self.messages.append({"role": "user", "content": CONTEXT_UNIVERSAL.format(datetime=datetime.now())})
        if user_id == self.__self:
            self.messages.append({"role": "user", "content": SELF_INSTRUCTIONS})
            self.messages.append({"role": "user", "content": CONTEXT_SELF})
        elif user_id in self.__friends:
            self.messages.append({"role": "user", "content": FRIEND_INSTRUCTIONS_TEMPLATE.format(user_id=user_id, user_display_name=user_display_name)})

        # Add context, but only for myself and friends
        if user_id in self.__friends or user_id == self.__self:
            self.messages.append({"role": "user", "content": CONTEXT_FRIENDS})
        else:
            self.messages.append({"role": "user", "content": CONTEXT_WORLD})

    def __call__(self, message):
        if self.user_id in self.__enemies:
            return "I don't talk to enemies."
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=self.messages)
        return completion.choices[0].message.content

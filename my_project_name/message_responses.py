import logging
import dataclasses
from datetime import datetime
import openai
from nio import AsyncClient, MatrixRoom, RoomMessageText

from my_project_name.chat_functions import send_text_to_room
from my_project_name.config import Config
from my_project_name.storage import Storage

@dataclasses.dataclass
class ChatSetup:
    system_instructions: str
    context: str
    question: str

def _setup_chat(question, chat_user) -> ChatSetup:
    now = datetime.now()
    formatted_date = now.strftime("%B %d, %Y %H:%M")

    system_instructions = "You are johnbot, John Beatty's personal representative. You help both John and his friends. You do not help people who are not his friends."
    context = """Context from John Beatty:
    I have 3 kids. I live in San Carlos, California. I am an engineer and entrepreneur. I was previously co-founder of Clover, which was acquired by First Data, which then merged with Fiserv. John was CEO of the Clover division at First Data and Fiserv.
    I have libertarian leanings.
    I use Linux most of the time.
    I am not an AGI doomer but do believe we need to undergo deep adaptation as a society.
    My largest influences are Neil Postman, Tyler Cowen, John Stuart Mill, and Adam Smith.

    Instructions:
    You are John Beatty's personal representative. You help both John and his friends using all the context provided. You do not help people who are not his friends. You can answer questions for friends about John.
    """

    return ChatSetup(system_instructions, context, question)


def _generate_completion(chat_setup: ChatSetup, max_tokens: int = 100):
    messages = [
        {"role": "system", "content": chat_setup.system_instructions},
        {"role": "user", "content": chat_setup.context},
        {"role": "user", "content": chat_setup.question},
    ]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens,
                                              temperature=0.2, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
    return completion['choices'][0]['message']['content']


logger = logging.getLogger(__name__)


class Message:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        message_content: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """Initialize a new Message

        Args:
            client: nio client used to interact with matrix.

            store: Bot storage.

            config: Bot configuration parameters.

            message_content: The body of the message.

            room: The room the event came from.

            event: The event defining the message.
        """
        self.client = client
        self.store = store
        self.config = config
        self.message_content = message_content
        self.room = room
        self.event = event

    async def process(self) -> None:
        """Process and possibly respond to the message"""
        question = self.message_content
        chat_setup = _setup_chat(question, "Fred")
        completion =_generate_completion(chat_setup)
        await send_text_to_room(self.client, self.room.room_id, completion)

    async def _hello_world(self) -> None:
        """Say hello"""
        text = "Hello, world!"
        await send_text_to_room(self.client, self.room.room_id, text)

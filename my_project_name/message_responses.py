import logging
from nio import AsyncClient, MatrixRoom, RoomMessageText

from my_project_name.chat_functions import send_text_to_room
from my_project_name.config import Config
from my_project_name.storage import Storage
from my_project_name.llm import ChatBot

logger = logging.getLogger(__name__)

chatbots = {}

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
        room_id = self.room.room_id
        user_id = self.event.sender
        user_display_name = self.room.display_name
        logger.info("Message from %s in room %s", user_id, room_id)
        if user_id not in chatbots:
            logger.info("Creating new chatbot for user %s", user_id)
            chatbots[user_id] = ChatBot(user_id, user_display_name)
        chatbot = chatbots[user_id]
        response = chatbot(self.message_content)
        await send_text_to_room(self.client, self.room.room_id, response)

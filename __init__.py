import logging
import random

from opsdroid.skill import Skill
from opsdroid.constraints import constrain_users
from opsdroid.matchers import match_event, match_regex
from opsdroid.events import Message
from opsdroid.connector.twitch.events import (
    DeleteMessage,
    UserFollowed,
    StreamStarted,
    UpdateTitle,
    BanUser, 
    UserJoinedChat
    )

_LOGGER = logging.getLogger(__name__)


class TwitchSkill(Skill):
    """Opsdroid skills for Twitch"""
    def __init__(self, opsdroid, config, *args, **kwargs):
        super().__init__(opsdroid, config, *args, **kwargs)
        self.connector = self.opsdroid.get_connector('twitch')
        self.twitter_connector = self.opsdroid.get_connector('twitter')
        
    @match_regex(r'^(hi|hello|hey|hallo|hows it going)(?:| @theflyingdev$)', case_sensitive=False)
    async def hello(self, message):
        text = random.choice(
            [
                f"Hello {message.user} hows it going?",
                f"Hey {message.user} welcome to the stream!",
                f"Hello {message.user} hows it going?",
                f"Hi {message.user} I hope you are having an awesome day!",
                f"Hey {message.user} glad you are here :D",
                f"Hello {message.user}, welcome and hope you brought pizza :p",
            ]
        )
        
        await self.connector.send(Message(text))
    
    @match_regex(r'bye( bye)?|see y(a|ou)|au revoir|gtg|I(\')?m off|goodbye', case_sensitive=False)
    async def bye(self, message):
        text = random.choice(
            [
                f"Thank you for watching {message.user} have a great day!",
                f"Good bye {message.user}, hope you have an awesome time",
                f"See you {message.user}, was nice chatting with you!",
                f"Have a good one {message.user}, thank you for watching"
            ]
        )
        
        await self.connector.send(Message(text))
   
    @match_regex(r'famous\? Buy followers', case_sensitive=False)
    async def remove_spam(self, message):
        await self.connector.send(BanUser(user=message.user))
        # deletion = DeleteMessage(id=message.event_id)
        # await self.connector.send(deletion)

    @match_event(StreamStarted)
    async def stream_started(self, event):
        _LOGGER.info("Stream started event received on skill!")
        await self.connector.send(Message(f"Hello everybody! Stream just started, today we are going to be working on {event.title}"))
        await self.twitter_connector.send(Message(f"I'm live on Twitch, today we are going to be working on - '{event.title}', come say hello! https://twitch.tv/{self.config['streamer-name']}"))

    @match_event(UserFollowed)
    async def user_followed(self, event):
        _LOGGER.info(f"User {event.follower} followed at {event.followed_at}")
        await self.connector.send(Message(f"Thank you so much for the follow {event.follower}, you are awesome!"))

    @match_regex(r'\!title (.*)')
    @constrain_users(self.config.get('whitelisted-users', []))
    async def change_title(self, message):
        _LOGGER.info("Attempt to change title")
        _LOGGER.info(message.regex.group(1))
        await self.connector.send(UpdateTitle(status=message.regex.group(1)))
        
    @match_event(Message)
    async def user_talked(self, message):
        _LOGGER.debug("{message.user} said {message.text} \n")
        await self.opsdroid.memory.put("talked", message.user)
    
    @match_event(UserJoinedChat)
    async def known_user_joined(self, event):
        _LOGGER.debug(f"{event.user} joined the chat \n")
        user = await self.opsdroid.memory.get("talked")
        
        if user and user not in self.config.get("blacklisted-users", []):
            text = random.choice(
                [
                    f"Welcome back to the stream {event.user}!",
                    f"How's it going {event.user}?",
                    f"It's great to see you {event.user}!",
                    f"Good to see you again {event.user} :D"
                ]
            )

            await self.connector.send(Message(text))

    @match_regex(r'\!set today (.*)')
    @constrain_users(self.config.get('whitelisted-users', []))
    async def set_today(self, message):
        _LOGGER.info("Setting today command")
        _LOGGER.info(message.regex.group(1))
        await self.opsdroid.memory.put("today", message.regex.group(1))

    @match_regex(r'!today|working today|doing today')
    async def today_command(self, message):
        today = await self.opsdroid.memory.get("today")
        
        await self.connector.send(Message(today.encode('utf-8')))

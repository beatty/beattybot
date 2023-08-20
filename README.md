# beattybot

A prototype personal Matrix bot for a large-language-model-based personal representative. The idea is that now that we have LLMs, we can easily build personal representative agents that people can talk to and make requests and offers to. Personal representatives can be talked to by people and/or their personal representatives.

This is based on the Nio template. See the original template README below for installation and usage instructions. After that, you need to do two things to customize for yourself:
 - Put your OPENAI_API_KEY in a file called .env in the root directory.
 - Modify llm.py to include identity, friends, enemies, etc. and adjust prompts and context to your liking. This is all static right now.

## Features
- User authentication comes for free
- Distinctive roles based on the agent's owner, family, friends, world, and enemies.
- Maintains conversation history with the sender (not persistent)
- Uses OpenAI for the LLM

## Roadmap
This is purely a prototype. There are many things that could be done to make this a general purpose framework, but that's not the goal of this project.

For the prototype, I'd like to add:
- The agent should reach out to you to route questions to you that it couldn't handle on its own (e.g. "Jane just let me know that she's going to be in SF this Friday. Do you want to meet up? It looks like you both have time at 2p")
- Persistent contexts that the owner can update through conversation (e.g. "tell my friends that I'll be in SF this Friday if anyone wants to meet up")
- Dynamic, continuous-scale friends list based on cosine similarity or vector distance using a trust graph.
- beattybot can listen in on all my conversations on my primary Matrix account and respond for me. If not, it would stay silent.
- Retrieval augmentation using the owner's sources of knowledge
- Experiment with LangChain and/or Semantic Kernel for goal planning and execution (https://github.com/microsoft/semantic-kernel)
- Experiment with simple tool use (e.g. https://til.simonwillison.net/llms/python-react-pattern)
- Experiment with non-OpenAI LLMs.

# Nio Template [![Built with matrix-nio](https://img.shields.io/badge/built%20with-matrix--nio-brightgreen)](https://github.com/poljar/matrix-nio) <a href="https://matrix.to/#/#nio-template:matrix.org"><img src="https://img.shields.io/matrix/nio-template:matrix.org?color=blue&label=Join%20the%20Matrix%20Room&server_fqdn=matrix-client.matrix.org" /></a>

A template for creating bots with
[matrix-nio](https://github.com/poljar/matrix-nio). The documentation for
matrix-nio can be found
[here](https://matrix-nio.readthedocs.io/en/latest/nio.html).

This repo contains a working Matrix echo bot that can be easily extended to your needs. Detailed documentation is included as well as a step-by-step guide on basic bot building.

Features include out-of-the-box support for:

* Bot commands
* SQLite3 and Postgres database backends
* Configuration files
* Multi-level logging
* Docker
* Participation in end-to-end encrypted rooms

## Projects using nio-template

* [anoadragon453/matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot
) - A matrix bot to remind you about things
* [gracchus163/hopeless](https://github.com/gracchus163/hopeless) - COREbot for the Hope2020 conference Matrix server
* [alturiak/nio-smith](https://github.com/alturiak/nio-smith) - A modular bot for @matrix-org that can be dynamically
extended by plugins
* [anoadragon453/msc-chatbot](https://github.com/anoadragon453/msc-chatbot) - A matrix bot for matrix spec proposals
* [anoadragon453/matrix-episode-bot](https://github.com/anoadragon453/matrix-episode-bot) - A matrix bot to post episode links
* [TheForcer/vision-nio](https://github.com/TheForcer/vision-nio) - A general purpose matrix chatbot
* [anoadragon453/drawing-challenge-bot](https://github.com/anoadragon453/drawing-challenge-bot) - A matrix bot to
post historical, weekly art challenges from reddit to a room
* [8go/matrix-eno-bot](https://github.com/8go/matrix-eno-bot) - A bot to be used as a) personal assistant or b) as 
an admin tool to maintain your Matrix installation or server
* [elokapina/bubo](https://github.com/elokapina/bubo) - Matrix bot to help with community management
* [elokapina/middleman](https://github.com/elokapina/middleman) - Matrix bot to act as a middleman, for example as a support bot
* [chc4/matrix-pinbot](https://github.com/chc4/matrix-pinbot) - Matrix bot for pinning messages to a dedicated channel

Want your project listed here? [Edit this
page!](https://github.com/anoadragon453/nio-template/edit/master/README.md)

## Getting started

See [SETUP.md](SETUP.md) for how to setup and run the template project.

## Project structure

*A reference of each file included in the template repository, its purpose and
what it does.*

The majority of the code is kept inside of the `my_project_name` folder, which
is in itself a [python package](https://docs.python.org/3/tutorial/modules.html),
the `__init__.py` file inside declaring it as such.

To run the bot, the `my-project-name` script in the root of the codebase is
available. It will import the `main` function from the `main.py` file in the
package and run it. To properly install this script into your python environment,
run `pip install -e .` in the project's root directory.

`setup.py` contains package information (for publishing your code to
[PyPI](https://pypi.org)) and `setup.cfg` just contains some configuration
options for linting tools.

`sample.config.yaml` is a sample configuration file. People running your bot
should be advised to copy this file to `config.yaml`, then edit it according to
their needs. Be sure never to check the edited `config.yaml` into source control
since it'll likely contain sensitive details such as passwords!

Below is a detailed description of each of the source code files contained within
the `my_project_name` directory:

### `main.py`

Initialises the config file, the bot store, and nio's AsyncClient (which is
used to retrieve and send events to a matrix homeserver). It also registering
some callbacks on the AsyncClient to tell it to call some functions when
certain events are received (such as an invite to a room, or a new message in a
room the bot is in).

It also starts the sync loop. Matrix clients "sync" with a homeserver, by
asking constantly asking for new events. Each time they do, the client gets a
sync token (stored in the `next_batch` field of the sync response). If the
client provides this token the next time it syncs (using the `since` parameter
on the `AsyncClient.sync` method), the homeserver will only return new event
*since* those specified by the given token.

This token is saved and provided again automatically by using the
`client.sync_forever(...)` method.

### `config.py`

This file reads a config file at a given path (hardcoded as `config.yaml` in
`main.py`), processes everything in it and makes the values available to the
rest of the bot's code so it knows what to do. Most of the options in the given
config file have default values, so things will continue to work even if an
option is left out of the config file. Obviously there are some config values
that are required though, like the homeserver URL, username, access token etc.
Otherwise the bot can't function.

### `storage.py`

Creates (if necessary) and connects to a SQLite3 database and provides commands
to put or retrieve data from it. Table definitions should be specified in
`_initial_setup`, and any necessary migrations should be put in
`_run_migrations`. There's currently no defined method for how migrations
should work though.

### `callbacks.py`

Holds callback methods which get run when the bot get a certain type of event
from the homserver during sync. The type and name of the method to be called
are specified in `main.py`. Currently there are two defined methods, one that
gets called when a message is sent in a room the bot is in, and another that
runs when the bot receives an invite to the room.

The message callback function, `message`, checks if the message was for the
bot, and whether it was a command. If both of those are true, the bot will
process that command.

The invite callback function, `invite`, processes the invite event and attempts
to join the room. This way, the bot will auto-join any room it is invited to.

### `bot_commands.py`

Where all the bot's commands are defined. New commands should be defined in
`process` with an associated private method. `echo` and `help` commands are
provided by default.

A `Command` object is created when a message comes in that's recognised as a
command from a user directed at the bot (either through the specified command
prefix (defined by the bot's config file), or through a private message
directly to the bot. The `process` command is then called for the bot to act on
that command.

### `message_responses.py`

Where responses to messages that are posted in a room (but not necessarily
directed at the bot) are specified. `callbacks.py` will listen for messages in
rooms the bot is in, and upon receiving one will create a new `Message` object
(which contains the message text, amongst other things) and calls `process()`
on it, which can send a message to the room as it sees fit.

A good example of this would be a Github bot that listens for people mentioning
issue numbers in chat (e.g. "We should fix #123"), and the bot sending messages
to the room immediately afterwards with the issue name and link.

### `chat_functions.py`

A separate file to hold helper methods related to messaging. Mostly just for
organisational purposes. Currently just holds `send_text_to_room`, a helper
method for sending formatted messages to a room.

### `errors.py`

Custom error types for the bot. Currently there's only one special type that's
defined for when a error is found while the config file is being processed.

## Questions?

Any questions? Please ask them in
[#nio-template:amorgan.xyz](https://matrix.to/#/!vmWBOsOkoOtVHMzZgN:amorgan.xyz?via=amorgan.xyz)
and we'll help you out!

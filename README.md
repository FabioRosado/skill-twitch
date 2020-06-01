# opsdroid skill weather

A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to work together with the Twitch Connector.

## Requirements

An active Twitch Connector.

## Configuration

```yaml
skills:
  twitch:
    streamer-name: TheFlyingDev
    #optional
    blacklisted-users:
      - <user 1>
      - <user 2>
    whitelisted-users:
      - <user 1>
```

## Usage

### hello

Opsdroid will reply to an hello message. It will choose from a few random messages.

> user: hello
>
> opsdroid: Hello <username from viewer> hows it going?

### Bye

Opsdroid will say goodbye to an user. It will choose from a few random messages.

> user: goodbye
>
> opsdroid: Thank you for watching <username from viewer> have a great day!


### Remove Span

Opsdroid will listen for chat messages and ban bots that will try to sell you followers and viewers.

> user: Want to be famous? Buy followers, viewers, subscribers and everything else!
>
> opsdroid: <removes and bans above message>

### Go live Event

Opsdroid will receive events from Twitch through webhooks and get notification when the streamer went live.

> <Streamer went live>
>
> Hello everybody! Stream just started, today we are going to be working on <channel title>

### User Followed Event

Opsdroid will receive following events from Twitch and get notifications when someone follows the streamer.

> <User follows streamer>
>
> Thank you so much for the follow <follower username>, you are awesome!

### !title

Opsdroid will set a new title for your Twitch channel - user needs to be set in the `whitelisted-users`.

> !title Working on opsdroid
>
> <channel title changed to "Working on opsdroid">

### Listen to users who talked on chat

Opsdroid will listen and keep track of users that talked on the chat.

> user: Oh yeah its awesome!
>
> <opsdroid stores user username to memory>

### User Joins Chat Event

Opsdroid will use memory to get the username of the user that got into the chat and welcome the user to the stream.

> <user joins the chat>
>
> opsdroid: It's great to see you again <username>!

### !set today 

Opsdroid will put to memory whatever you are working on today - user needs to be set in the `whitelisted-users`.

> user: !set today "Working on Twitch connector for opsdroid"
>
> <opsdroid puts "Working on Twitch connector for opsdroid" on to the !today command>

### !today

Opsdroid will get the last set today command and send it to the channel.

> user: !today
>
> opsdroid: Working on Twitch connector for opsdroid
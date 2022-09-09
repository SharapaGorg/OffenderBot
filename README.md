# Offender Bot

## Quick start

**Install dependencies**

```
pip install -r requirements.py
```

**Crate and fill config.py**

```
TOKEN = 'bot token here'
```

**Launch bot**

```
python main.py
```

## Hierarchy

- **Moderator** - can edit global settings of bot
- **Admin** - can edit local settings of group/chat
- **Chat member** - dummy

## Database

- **admins** - list of admins
- **moderators** - list of administrators
- **properties** - options, that help to offend better
- **phrases** - list of phrases for different names
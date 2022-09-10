"""

Methods to interact with table named moderators

- get_moderators(user_id : str = None, username : str = None)
- add_moderator(user_id : str, username : str)
- delete_property(user_id : str = None, username : str = None)

"""

from sqlalchemy import *

from controller import Session
from models import Moderator

def get_moderators(user_id : str = None, username : str = None) -> list:
    _session = Session()

    moders = select(Moderator).where(Moderator.user_id == user_id)

    if username is not None:
        moders = moders.where(Moderator.username == username)

    result = list(_session.scalars(moders))
    return result

def add_moderator(user_id : str, username : str) -> Moderator:
    moder = Moderator(
        user_id = user_id,
        username = username
    )

    _session = Session()

    _session.add(moder)
    _session.commit()

    _session.close()

    return moder

def delete_moderator(user_id : str = None, username : str = None) -> None:
    _session = Session()
    moders = get_moderators(user_id, username)

    for moder in moders:
        _session.delete(moder)
        _session.commit()

    _session.close()
"""

Methods to interact with table named phrases

- get_phrases(name : str = None, phrase : str = None)
- add_phrase(name : str, phrase : str)
- delete_property(name : str, phrase : str)

"""

from sqlalchemy import *

from controller import Session
from models import Phrase

def get_phrases(name : str = None, phrase : str = None) -> list:
    _session = Session()

    phrases = select(Phrase)

    if name is not None:
        phrases = phrases.where(Phrase.name == name)

    if phrase is not None:
        phrases = phrases.where(Phrase.phrase == phrase)

    result = list(_session.scalars(phrases))
    _session.close()

    return result

def add_phrase(name : str, phrase : str) -> Phrase:
    phrase = Phrase(
        name = name,
        phrase = phrase
    )

    _session = Session()

    _session.add(phrase)
    _session.commit()

    _session.close()

    return phrase

def delete_phrase(name : str, phrase : str) -> None:
    _session = Session()
    phrases = get_phrases(name, phrase)

    for phrase in phrases:
        _session.delete(phrase)
        _session.commit()

    _session.close()
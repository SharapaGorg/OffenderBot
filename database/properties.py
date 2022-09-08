"""

Methods to interact with table named properties

- get_properties(channel_id : str, user_id : str = None, value : str = None)
- add_property(user_id : str, channel_id : str, value : str)
- delete_property(user_id : str, channel_id : str, value : str)

"""

from sqlalchemy import *

from controller import Session
from models import Property


def get_properties(
    channel_id: str,
    user_id: str = None,
    value: str = None
) -> list[Property]:

    _session = Session()

    properties = select(Property).where(Property.channel_id == channel_id)

    if user_id is not None:
        properties = properties.where(Property.user_id == user_id)

    if value is not None:
        properties = properties.where(Property.value == value)

    result = list(_session.scalars(properties))
    _session.close()

    return result


def add_property(
    user_id: str,
    channel_id: str,
    value: str
) -> Property:

    property = Property(
        user_id=user_id,
        channel_id=channel_id,
        value=value
    )

    _session = Session()

    _session.add(property)
    _session.commit()

    _session.close()

    return property


def delete_property(
    user_id: str,
    channel_id: str,
    value: str
) -> None:

    _session = Session()
    properties = get_properties(channel_id, user_id, value)

    for prop in properties:
        _session.delete(prop)
        _session.commit()

    _session.close()

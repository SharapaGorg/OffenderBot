"""

Methods to interact with table named admins

- get_admins(channel_id : str = None, user_id : str = None)
- add_admin(user_id : str, channel_id : str)
- delete_admin(user_id : str, channel_id : str)

"""

from sqlalchemy import *

from controller import Session
from models import Admin


def get_admins(
    channel_id: str = None,
    user_id: str = None
) -> list:

    _session = Session()

    admins = None

    if channel_id is not None:
        admins = select(Admin).where(Admin.channel_id == channel_id)

    if user_id is not None:
        if admins is not None:
            admins = admins.where(Admin.user_id == user_id)
        else:
            admins = select(Admin).where(Admin.user_id == user_id)

    result = list(_session.scalars(admins))
    _session.close()

    return result


def add_admin(
    user_id: str,
    channel_id: str,
) -> Admin:

    admin = Admin(
        user_id=user_id,
        channel_id=channel_id,
    )

    _session = Session()

    _session.add(admin)
    _session.commit()

    _session.close()

    return admin


def delete_admin(
    user_id: str = None,
    channel_id: str = None,
) -> None:

    _session = Session()
    admins = get_admins(channel_id, user_id)

    for admin in admins:
        _session.delete(admin)
        _session.commit()

    _session.close()

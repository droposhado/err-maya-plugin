"""Main file for maya plugin"""
import datetime
import os
import uuid

from errbot import BotPlugin, botcmd
from sqlalchemy.orm import sessionmaker

from model import LiquidModel, engine

ERR_MAYA_CLIENT_NAME = os.getenv('ERR_MAYA_CLIENT_NAME', 'err-maya-plugin')
ERR_MAYA_CLIENT_VERSION = os.getenv('ERR_MAYA_CLIENT_VERSION', '1.1.0')

DATETIME_ISO8601_FULL_MASK = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_ISO8601_SIMPLE_MASK = '%Y-%m-%d'
DATETIME_HOUR_MASK = '%H:%M:%S'

Session = sessionmaker(bind=engine)
session = Session()


class MayaPlugin(BotPlugin):
    """
    Base class to maya project
    """

    @botcmd(split_args_with=None)
    def maya_liquid_list(self, msg, args):
        """
        List of liquid consumed today or on a specific date.
        """

        if len(args) < 1:
            return "Please use '/maya liquid list <type>'"

        liq_type = args[0].lower()

        if len(args) == 2:
            try:
                now = datetime.datetime.strptime(args[1],
                                                 DATETIME_ISO8601_SIMPLE_MASK)
            except ValueError:
                return "Please use a valid datetime in ISO8601 (YYYY-MM-DD)"

        else:
            now = datetime.datetime.utcnow()

        query_filters = [
            LiquidModel.creation_date > datetime.datetime(now.year,
                                                          now.month,
                                                          now.day, 0, 0, 0),
            LiquidModel.creation_date < datetime.datetime(now.year,
                                                          now.month,
                                                          now.day, 23, 59, 59),
            LiquidModel.type == liq_type
        ]
        liquids = LiquidModel().query.filter(*query_filters)

        liner = str()
        total = 0
        for liquid in liquids:
            date_str = liquid.creation_date.strftime(DATETIME_HOUR_MASK)
            liner += date_str + "    " + str(liquid.quantity) + "\n"
            total += liquid.quantity

        liner += "\nTotal " + str(total)

        return liner

    @botcmd(split_args_with=None)
    def maya_liquid_add(self, msg, args):
        """
        Adds an amount of liquid consumed
        """

        if len(args) < 2:
            return "Please use '/maya liquid add <type> <quantity>'"

        liq_type = args[0].lower()
        value = args[1]

        try:
            value = int(value)

        except ValueError:
            return "Please enter a valid quantity"

        if len(args) == 3:
            try:
                now = datetime.datetime.strptime(args[2],
                                                 DATETIME_ISO8601_FULL_MASK)
            except ValueError:
                return "Please use a valid datetime in ISO8601 (YYYY-MM-DDTHH:MM:SSZ)"

        else:
            now = datetime.datetime.utcnow()

        liquid = LiquidModel(
            id=uuid.uuid4(),
            client_name=ERR_MAYA_CLIENT_NAME,
            client_version=ERR_MAYA_CLIENT_VERSION,
            creation_date=now,
            last_modification=now,
            quantity=value,
            unit='ml',
            type=liq_type,
            username=msg.frm.fullname
        )

        session.add(liquid)
        session.commit()

        uuid_str = liquid.id
        return f"{value}ml of {liq_type} was drunk. ({uuid_str})"

    @botcmd(split_args_with=None)
    def maya_liquid_remove(self, msg, args):
        """
        Remove a specific item using its UUID.
        """

        if len(args) < 2:
            return "Please use '/maya liquid remove <type> <uuid>'"

        liq_type = args[0].lower()
        value = args[1]

        try:
            uuid_instance = uuid.UUID(value)

        except ValueError:

            return "Please use a valid UUID"

        found = session.query(LiquidModel).get(uuid_instance)
        if found is None:
            return f"UUID {value} to {liq_type} not found"

        found_id = found.id
        if str(found_id) != value:
            return f"UUID mismatch between {found_id} (database) and {value} (input)"

        session.delete(found)
        session.commit()

        return f"{value} was removed."

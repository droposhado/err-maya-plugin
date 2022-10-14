"""Main file for maya plugin"""
import datetime
import os
import uuid
from enum import Enum

import mongoengine
from errbot import BotPlugin, botcmd

ERR_MAYA_MONGODB_URL = os.getenv('ERR_MAYA_MONGODB_URL',
                                 'mongodb://localhost:27017')

ERR_MAYA_CLIENT_NAME = os.getenv('ERR_MAYA_CLIENT_NAME', 'err-maya-plugin')
ERR_MAYA_CLIENT_VERSION = os.getenv('ERR_MAYA_CLIENT_VERSION', '1.0.0')

ERR_MAYA_PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'manual')
ERR_MAYA_PROVIDER_VERSION = os.getenv('PROVIDER_VERSION', None)

DATETIME_ISO8601_FULL_MASK = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_ISO8601_SIMPLE_MASK = '%Y-%m-%d'
DATETIME_HOUR_MASK = '%H:%M:%S'


class User(mongoengine.EmbeddedDocument):
    """Store Discord user information"""
    person = mongoengine.StringField()
    nick = mongoengine.StringField()
    fullname = mongoengine.StringField()
    client = mongoengine.StringField()
    email = mongoengine.StringField()


class Client(mongoengine.EmbeddedDocument):
    """Store information about client used"""
    name = mongoengine.StringField()
    version = mongoengine.StringField()


class Provider(mongoengine.EmbeddedDocument):
    """Store information about provider used"""
    name = mongoengine.StringField()
    version = mongoengine.StringField()


class LiquidUnit(Enum):
    """Units of liquid"""
    ML = "ml"
    L = "l"


class Liquid(mongoengine.Document):
    """Liquid as base class"""

    meta = {
        'abstract': True
    }

    date = mongoengine.DateTimeField()
    last_modification = mongoengine.DateTimeField()
    quantity = mongoengine.IntField()
    uuid = mongoengine.UUIDField()
    active = mongoengine.BooleanField()
    client = mongoengine.EmbeddedDocumentField(Client)
    provider = mongoengine.EmbeddedDocumentField(Provider)
    user = mongoengine.EmbeddedDocumentField(User)
    unit = mongoengine.EnumField(LiquidUnit, default=LiquidUnit.ML)


class Water(Liquid):
    """Water model and collection"""


class Coffee(Liquid):
    """Coffee model and collection"""


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

        if liq_type == "water":
            liquid = Water

        elif liq_type == "coffee":
            liquid = Coffee

        else:
            return "Not supported type"

        if len(args) == 2:
            try:
                now = datetime.datetime.strptime(args[1], DATETIME_ISO8601_SIMPLE_MASK)
            except ValueError:
                return "Please use a valid datetime in ISO8601 (YYYY-MM-DD)"

        else:
            now = datetime.datetime.utcnow()

        mongoengine.connect(host=ERR_MAYA_MONGODB_URL,
                            uuidRepresentation='standard')

        found_docs = liquid.objects(
            date__gt=datetime.datetime(now.year, now.month, now.day, 0, 0, 0),
            date__lt=datetime.datetime(now.year, now.month, now.day, 23, 59, 59))

        liner = str()
        total = 0
        for doc in found_docs:
            date_str = doc.date.strftime(DATETIME_HOUR_MASK)
            liner += date_str + "    " + str(doc.quantity) + "\n"
            total += doc.quantity

        liner += "\nTotal " + str(total)

        mongoengine.disconnect()

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

        if liq_type == "water":
            liquid = Water()

        elif liq_type == "coffee":
            liquid = Coffee()

        else:
            return "Not supported type"

        if len(args) == 3:
            try:
                now = datetime.datetime.strptime(args[2], DATETIME_ISO8601_FULL_MASK)
            except ValueError:
                return "Please use a valid datetime in ISO8601 (YYYY-MM-DDTHH:MM:SSZ)"

        else:
            now = datetime.datetime.utcnow()

        mongoengine.connect(host=ERR_MAYA_MONGODB_URL,
                            uuidRepresentation='standard')

        liquid.uuid = uuid.uuid4()
        liquid.quantity = value
        liquid.unit = LiquidUnit.ML
        liquid.date = now
        liquid.last_modification = now

        client = Client()
        client.name = ERR_MAYA_CLIENT_NAME
        client.version = ERR_MAYA_CLIENT_VERSION
        liquid.client = client

        provider = Provider()
        provider.name = ERR_MAYA_PROVIDER_NAME
        provider.version = ERR_MAYA_PROVIDER_VERSION
        liquid.provider = provider

        user_info = msg.frm
        user = User()
        user.person = user_info.person
        user.nick = user_info.nick
        user.fullname = user_info.fullname
        user.client = user_info.client
        user.email = user_info.email
        liquid.user = user

        liquid.save()

        mongoengine.disconnect()

        unit = LiquidUnit.ML.value
        uuid_str = liquid.uuid
        return f"{value}{unit} of {liq_type} was drunk. ({uuid_str})"

    @botcmd(split_args_with=None)
    def maya_liquid_remove(self, msg, args):
        """
        Remove a specific item using its UUID.
        """

        if len(args) < 2:
            return "Please use '/maya liquid remove <type> <uuid>'"

        liq_type = args[0].lower()
        value = args[1]

        if liq_type == "water":
            liquid = Water

        elif liq_type == "coffee":
            liquid = Coffee

        else:
            return "Not supported type"

        try:
            uuid_instance = uuid.UUID(value)

        except ValueError:

            return "Please use a valid UUID"

        mongoengine.connect(host=ERR_MAYA_MONGODB_URL,
                            uuidRepresentation='standard')

        found_doc = liquid.objects(uuid=uuid_instance).first()
        if found_doc is None:
            mongoengine.disconnect()
            return f"UUID {value} to {liq_type} not found"

        fnd_uuid = found_doc.uuid
        if str(fnd_uuid) != value:
            mongoengine.disconnect()
            return f"UUID mismatch between {fnd_uuid} (database) and  {value} (input)"

        found_doc.delete()
        mongoengine.disconnect()

        return f"{value} was removed."

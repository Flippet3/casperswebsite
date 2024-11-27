import os
import json
from functools import cache
from platform import system

IS_LOCAL = bool(int(os.environ.get("IS_LOCAL", "windows" in system().lower())))


def get_base_folder():
    basepath = os.path.abspath(".").split("casperswebsite")[0] + "casperswebsite/src/"
    return basepath


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


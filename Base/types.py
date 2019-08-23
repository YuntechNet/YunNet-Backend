from enum import IntEnum


class LockTypes(IntEnum):
    ABUSE = 0
    OVERFLOW = 1
    VIRUS = 2


class IpStatus(IntEnum):
    UNLOCK = 0
    LOCK = 1
    UNLIMITED = 2


class IpTypes(IntEnum):
    UNUSED = 0
    DORM_NORMAL = 1
    DORM_PANDA = 2
    SERVICE = 3
    SWITCH = 4

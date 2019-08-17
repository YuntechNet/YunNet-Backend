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
    DORM_NORMAL = 0
    DORM_PANDA = 1
    SERVICE = 2
    SWITCH = 3
    UNUSED = 4

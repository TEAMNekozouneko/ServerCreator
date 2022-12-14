from enum import Enum

class Platform(Enum):
    WINDOWS = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"
    JAVA = "Java"

    @staticmethod
    def valueOf(v: str):
        for e in Platform:
            if (e.value.lower() == v.lower() or e.name.lower() == v.lower()):
                return e
        return None

class Architecture(Enum):
    X64 = "x64"
    X32 = "x32"
    ARM64 = "aarch64"
    ARM32 = "armhf"
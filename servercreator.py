print("Starting...")
import requests, platform, time, tqdm, subprocess, tarfile, shutil, os, glob
import util
from enums import *

print(f"Platform: {platform.python_implementation()} v{platform.python_version()} on {platform.system()} {platform.release()}")
print("Initializing variables...")

__sic = {
    "bedrock": "BE: 統合版",
    "modded": "JE: Mod (Forge/Fabric) (子サーバー)",
    "proxies": "JE: マイクラ中継サーバー (子サーバー必須)",
    "servers": "JE: マイクラサーバー (子サーバー)",
    "vanilla": "JE: バニラサーバー (子サーバー)"
}
__si = {
    # proxies

    "bungeecord": {
        "name": "BungeeCord [Plugin (Bungee)]",
        "level": 1,
        "deprecated": False
    },
    "velocity": {
        "name": "Velocity [Plugin (Velocity)]",
        "level": 1,
        "deprecated": False
    },
    "waterfall": {
        "name": "Waterfall [Plugin (Bungee/Waterfall)]",
        "level": 1,
        "deprecated": False
    },
    "flamecord": {
        "name": "FlameCord [Plugin (Bungee/Waterfall)]",
        "level": 1,
        "deprecated": False
    },

    # modded

    "mohist": {
        "name": "Mohist [Mod (Forge)+Plugin (Spigot)]",
        "level": 3,
        "deprecated": False
    },
    "forge": {
        "name": "Forge [Mod (Forge)]",
        "level": 3,
        "deprecated": False
    },
    "catserver": {
        "name": "CatServer [Mod (Forge)+Plugin (Spigot)]",
        "level": 3,
        "deprecated": False
    },
    "fabric": {
        "name": "Fabric [Mod (Fabric)]",
        "level": 2,
        "deprecated": False
    },

    # servers

    "bukkit": {
        "name": "Bukkit [Plugin (Bukkit)]",
        "level": 3,
        "deprecated": True
    },
    "paper": {
        "name": "Paper [Plugin (Spigot/Paper)]",
        "level": 2,
        "deprecated": False
    },
    "spigot": {
        "name": "Spigot [Plugin (Spigot)]",
        "level": 3,
        "deprecated": False
    },
    "purpur": {
        "name": "Purpur [Plugin (Spigot/Paper)]",
        "level": 1,
        "deprecated": False
    },
    "tuinity": {
        "name": "Tuinity [Plugin (Spigot/Paper)]",
        "level": 2,
        "deprecated": True
    },
    "sponge": {
        "name": "Sponge (Vanilla?) [Plugin (Sponge)]",
        "level": 2,
        "deprecated": False
    },
    
    # vanilla
    
    "vanilla": {
        "name": "Vanilla",
        "level": 3,
        "deprecated": False
    },
    "snapshot": {
        "name": "Snapshot",
        "level": 3,
        "deprecated": False
    },

    # bedrock

    "nukkitx": {
        "name": "NukkitX",
        "level": 2,
        "deprecated": False
    },
    "pocketmine": {
        "name": "PocketMine",
        "level": 1,
        "deprecated": False
    }

}
__jr = {
    Platform.WINDOWS: {
        "17": {
            "aarch64": ("https://aka.ms/download-jdk/microsoft-jdk-17.0.5-windows-aarch64.zip", ".zip"),
            "x64": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-win_x64.zip", ".zip"),
            "x32": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-win_i686.zip", ".zip")
        },
        "16": {
            "aarch64": ("https://aka.ms/download-jdk/microsoft-jdk-16.0.2.7.1-windows-aarch64.zip", ".zip"),
            "x64": ("https://github.com/adoptium/temurin16-binaries/releases/download/jdk16u-2022-01-04-15-53-beta/OpenJDK16U-jdk_x64_windows_hotspot_2022-01-04-15-53.zip", ".zip"),
            "x32": "https://github.com/adoptium/temurin16-binaries/releases/download/jdk16u-2022-01-04-15-53-beta/OpenJDK16U-jdk_x86-32_windows_hotspot_2022-01-04-15-53.zip"   
        },
        "8": {
            "aarch64": ("https://aka.ms/download-jdk/microsoft-jdk-11.0.17-windows-aarch64.zip", ".zip"), # Java 11
            "x64": ("https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u352-b05-ea/OpenJDK8U-jre_x64_windows_hotspot_8u352b05_ea.zip", ".zip"),
            "x32": ("https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u352-b05-ea/OpenJDK8U-jre_x86-32_windows_hotspot_8u352b05_ea.zip", ".zip")
        }
    },
    Platform.MAC: {
        "17": {
            "aarch64": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-macosx_aarch64.zip", ".zip"),
            "x64": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-macosx_x64.zip", ".zip")
        },
        "16": {
            "aarch64": ("https://aka.ms/download-jdk/microsoft-jdk-16.0.2.7.1-macOS-aarch64.tar.gz", ".tar.gz"),
            "x64": ("https://aka.ms/download-jdk/microsoft-jdk-16.0.2.7.1-macOS-x64.tar.gz", ".tar.gz")
        },
        "8": {
            "aarch64": ("https://cdn.azul.com/zulu/bin/zulu8.66.0.15-ca-jdk8.0.352-macosx_aarch64.zip", ".zip"),
            "x64": ("https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u352-b05-ea/OpenJDK8U-jdk_x64_mac_hotspot_8u352b05_ea.tar.gz", ".tar.gz")
        }
    },
    Platform.LINUX: {
        "17": {
            "aarch64": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-linux_aarch64.tar.gz", ".tar.gz"),
            "x64": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-linux_x64.zip", ".zip"),
            "x32": ("https://cdn.azul.com/zulu/bin/zulu17.38.21-ca-jdk17.0.5-linux_i686.zip", ".zip")
        },
        "16": {
            "aarch64": ("https://github.com/adoptium/temurin16-binaries/releases/download/jdk16u-2022-01-04-15-53-beta/OpenJDK16U-jdk_aarch64_linux_hotspot_2022-01-04-15-53.tar.gz", ".tar.gz"),
            "x64": ("https://aka.ms/download-jdk/microsoft-jdk-16.0.2.7.1-linux-x64.tar.gz", "tar.gz"),
            "x32": ("https://aka.ms/download-jdk/microsoft-jdk-16.0.2.7.1-linux-aarch64.tar.gz", ".tar.gz")
        },
        "8": {
            "aarch64": ("https://cdn.azul.com/zulu-embedded/bin/zulu8.66.0.15-ca-jdk8.0.352-linux_aarch64.tar.gz", ".tar.gz"),
            "x64": ("https://cdn.azul.com/zulu/bin/zulu8.66.0.15-ca-jdk8.0.352-linux_x64.zip", ".zip"),
            "x32": ("https://cdn.azul.com/zulu/bin/zulu8.66.0.15-ca-jdk8.0.352-linux_i686.zip", ".zip")
        }
    }
}
__l = {1: "軽い", 2: "軽め", 3: "重い"}


def main():
    arch: Architecture
    print("------------------------------------------------------------------------------------")
    print("Server Creator v0.0-dev")
    print("By Team Nekozouneko (Source code: https://github.com/TeamNekozouneko/ServerCreator )")
    print("------------------------------------------------------------------------------------")
    print("Checking platform...")
    print(f"Detected: {platform.system()} {'x64' if util.is_64bits() else 'x32 (x86?)'}")
    isCorrect = input("ARMのアーキテクチャを使用していますか? ([Y]es/[N]o [Default: No]): ")
    a = util.yncheck(isCorrect, False)

    if util.is_64bits():
        if a: arch = Architecture.ARM64
        else: arch = Architecture.X64
    else:
        if a: arch = Architecture.ARM32
        else: arch = Architecture.X32
    
    pf = Platform.valueOf(platform.system())
    
    if arch == Architecture.ARM32:
        print("Architecture arm32 (armhf) is not supported!")
        return
    
    ftres:dict = requests.get("https://serverjars.com/api/fetchTypes/").json()

    print("----------------------------------- SERVER TYPE -----------------------------------")
    
    for r in ftres["response"].keys():
        print(f"- {__sic[r]}")
        for r1 in ftres["response"][r]:
            if (r1 == "pocketmine"): continue
            print(f"\t[{__l[__si[r1]['level']]}] {__si[r1]['name']}")
        time.sleep(.5)

    print("-------------------------------------------------------------------------------------")

    typeres = input("サーバータイプを選択: ")
    cate: str
    while True:
        if (typeres == "" or typeres is None or util.isSpaceOnly(typeres)):
            print("ERR: 返答が空白です")
            typeres = input("サーバータイプを選択: ")
            continue
        else:
            for c in ftres["response"].keys():
                if typeres in ftres["response"][c] and typeres.lower() != "pocketmine":
                    cate = c
                    break
            else:
                print("ERR: 存在しないまたはサポートされていないサーバータイプです")
                typeres = input("サーバータイプを選択: ")
            break
    
    print("-------------------------------------- VERSION --------------------------------------")

    vres:dict = requests.get(f"https://serverjars.com/api/fetchAll/{cate}/{typeres}").json()["response"]
    vs = "\t"
    for b in vres:
        vs = vs + f"{b['version']}\t"
    print(vs)

    vtres = input("バージョンを選択: ")
    while True:
        if (vtres is None or vtres == "" or util.isSpaceOnly(vtres)):
            print("ERR: 返答が空白です")
            vtres = input("バージョンを選択: ")
            continue
        else:
            for b in vres:
                if (b['version'] == vtres):
                    break
            else:
                print("ERR: 存在しないバージョンです")
                vtres = input("バージョンを選択: ")
                continue
            break

    print("--------------------------------- DOWNLOAD SERVER ---------------------------------")
    fn = f"{typeres}-{vtres}.jar"
    s:int = requests.get(f"https://serverjars.com/api/fetchDetails/{cate}/{typeres}/{vtres}").json()["response"]["size"]["bytes"]

    print(f"Starting {fn} download process...")
    jard = requests.get(f"https://serverjars.com/api/fetchJar/{cate}/{typeres}/{vtres}", stream=True)
    bar = tqdm.tqdm(total=s, unit="B", unit_scale=True)
    bar.set_description(f"{fn}")
    with open(fn, "wb") as f:
        for chunk in jard.iter_content(chunk_size=1024):
            f.write(chunk)
            bar.update(len(chunk))
        bar.close()
    print("--------------------------------------- JAVA ---------------------------------------")
    ujv: str = "8"
    if cate == "servers" or cate == "vanilla" or cate == "modded":
        if typeres == "snapshot":
            ujv = "17"
        elif "1.18" in vtres or "1.19" in vtres:
            ujv = "17"
        elif "1.17" in vtres:
            ujv = "16"

    jres = util.yncheck(input("Javaを自動でダウンロードしますか? ([Y]es/[N]o [Default: Yes]): "), True)
    print(jres)
    if jres:
        jdu = __jr[pf][ujv][arch.value]
        js = float(requests.head(jdu[0]).headers["content-length"])
        jbar = tqdm.tqdm(desc=f"Java {ujv}", total=js, unit="B", unit_scale=True)
        jds = requests.get(jdu[0], stream=True)
        with open(f"java{jdu[1]}", "wb") as j:
            for chunk in jds.iter_content(1024):
                j.write(chunk)
                jbar.update(len(chunk))
            jbar.close()
        
        print("Extracting java...")

        if (jdu[1] == ".tar.gz"):
            with tarfile.open(f"java.tar.gz", "r:gz") as jtar:
                jtar.extractall(path="java")
        else:
            shutil.unpack_archive("java.zip")
        
        print("Searching java dir...")
        jdirs = util.fetchJavaDirs()
        
        print(jdirs)

if __name__ == "__main__":
    main()
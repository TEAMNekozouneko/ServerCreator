import requests, shutil, tarfile, tqdm, os, time
import util
from enums import *

def server_type(ol: dict[int, str], si, sic):
    ftres:dict = requests.get("https://serverjars.com/api/fetchTypes/").json()
    for r in ftres["response"].keys():
        print(f"- {sic[r]}")
        for r1 in ftres["response"][r]:
            if (r1 == "pocketmine"): continue
            print(f"\t[{ol[si[r1]['level']]}] {si[r1]['name']}")
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
    
    return (typeres, cate)

def serv_version(category, server_type):
    vres:dict = requests.get(f"https://serverjars.com/api/fetchAll/{category}/{server_type}").json()["response"]
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
    
    return vtres

def java(plat: Platform, arch: Architecture,  javarepo: dict, category: str, servtype: str, ver: str, jver: str = None):
    if jver is None or jver not in ["8", "16", "17"]:
        jver: str = "8"
        if category == "servers" or category == "vanilla" or category == "modded":
            if servtype == "snapshot":
                jver = "17"
            elif "1.18" in ver or "1.19" in ver:
                jver = "17"
            elif "1.17" in ver:
                jver = "16"

    jres = util.yncheck(input("Javaを自動でダウンロードしますか? ([Y]es/[N]o [Default: Yes]): "), True)
    if jres:
        cjdirs = util.fetchJavaDirs()
        if len(cjdirs) >= 1:
            print("WARN: Javaの実行ファイルが検出されました:")
            for cjdir in cjdirs:
                print(f"- {cjdir}")
            print("WARN: 以上のJavaフォルダが検出されました。")
            ansrm = util.yncheck(input("以上のフォルダを削除してよろしいですか? ([Y]es/[N]o [Default: Yes]): "), True)

            if ansrm:
                for cjdir in cjdirs:
                    print(f"Removing {cjdir}")
                    shutil.rmtree(cjdir)

        jdu = javarepo[plat][jver][arch.value]
        js = int(requests.head(jdu[0]).headers["content-length"])
        print(str.format("Total size: {0}", js))
        jbar = tqdm.tqdm(desc=f"Java {jver}", total=js, unit="B", unit_scale=True)
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
        
        try:
            os.remove(f"java{jdu[1]}")
        except:
            print(f"Cant remove java archive (java{jdu[1]})")
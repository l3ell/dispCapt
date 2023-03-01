import glob
import subprocess

LANGUAGE = "eng"

WORK_PATH = "/work"
INPUT_PATH = WORK_PATH + "/src/"
OUTPUT_PATH = WORK_PATH + "/dst/"

# 入力フォルダ内のファイルを全て変換する
inputFiles = glob.glob(INPUT_PATH + "*")
for inputFile in inputFiles:
    # 入力
    fileName = inputFile.split("/")[-1]
    src = INPUT_PATH + fileName
    # 出力
    fileNameWoExt = fileName.split(".")[0]
    dst = OUTPUT_PATH + fileNameWoExt
    # 変換
    cmdLst = [
        "tesseract",
        src,
        dst,
        "-l",
        LANGUAGE,
    ]
    subprocess.run(cmdLst)

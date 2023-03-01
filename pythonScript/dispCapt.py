import os

import pyautogui
# from PIL import ImageGrab, Image
from PIL import ImageGrab
import cv2
import numpy

OUTPUT_PATH = "./clipboardImg/"
OUTPUT_NAME_CAPT = "img"
OUTPUT_NAME_UNION = "union"
OUTPUT_NAME_MASK = "mask"
OUTPUT_EXT = ".png"

# キャプチャ完了するとみなす一致率(パーセンテージを10倍した値)
FINISH_RATE_CPT = 995

SHAPE_HEIGHT = 0
SHAPE_WIDTH = 1

SHAPE_X = 0
SHAPE_Y = 1


# 共通するファイル名を扱うことが多い
# C言語のようにマクロ定義できるか知らないので
# 関数化してミスを防ぐ
# 入力：ファイル名の差分となるインデックス(int)
# 出力：ファイル名（パス・ファイル名・拡張子）
def genOutPutFileName(idx_r):
    fileName = OUTPUT_PATH + OUTPUT_NAME_CAPT + str(idx_r) + OUTPUT_EXT
    return fileName


# 2つのimgを比較し、その一致率を取得する
# 入力1：比較用img1
# 入力2：比較用img2
# 入力3：倍率として換算するための画像サイズ
# 出力：一致率(パーセンテージの10倍値)
def getMatchRate(cmp1_r, cmp2_r, imgSize_r):
    if 0 != imgSize_r:
        chkZero = numpy.count_nonzero(cmp1_r == cmp2_r)
        matchRate = chkZero / imgSize_r * 100
        # print("一致率: " + "{:.2f}".format(matchRate) + "%")

        percentage = int(matchRate * 10)

    else:
        percentage = 0

    return percentage


# ウィンドウをキャプチャする
# 入力：キャプチャ時に保存したいファイル名(パス・ファイル名・拡張子が必要)
# 出力(ファイル)：キャプチャした画像
def getWindowImg(imgName_r):
    # 選択中のウィンドウをキャプチャする
    pyautogui.hotkey("alt", "prtscr")

    # キャプチャした画像をファイルへ保存する
    img = ImageGrab.grabclipboard()
    if img is None:
        print("画面キャプチャに失敗しています")
        return
    img.save(imgName_r)


# 画面をスクロールしながらキャプチャする
# 出力(戻り値)：キャプチャした回数
def getPageImg():
    print("キャプチャを開始します。")
    # ウィンドウを切り替える
    pyautogui.hotkey("alt", "tab")

    # ウィンドウの先頭まで移動する
    pyautogui.hotkey("ctrl", "home")

    # スクロールできなくなるまで繰り返しキャプチャする
    cptCnt = 0
    while (1):
        # ウィンドウキャプチャして画像として保存する
        nowCntImgName = genOutPutFileName(cptCnt)
        getWindowImg(nowCntImgName)

        # 2つ以上の画像をキャプチャしたら一致度を確認する
        if 1 <= cptCnt:
            befCntImgName = genOutPutFileName(cptCnt-1)
            nowCntImg = cv2.imread(nowCntImgName)
            befCntImg = cv2.imread(befCntImgName)
            matchRate = getMatchRate(nowCntImg, befCntImg, nowCntImg.size)

            # ある程度一致したら終了する
            if FINISH_RATE_CPT < matchRate:
                print("キャプチャを終了します。")
                os.remove(nowCntImgName)
                break

        # 次のキャプチャに進む
        pyautogui.press("pagedown")
        cptCnt = cptCnt + 1

    return cptCnt


# キャプチャした画像のうち、2枚の画像に共通する部分をヘッダーとして取得する
# Warning：同じサイズのimgを2つ指定すること
# 入力1：共通部分を取得したい画像のimg1
# 入力2：共通部分を取得したい画像のimg2
# 出力：ヘッダに相当するimg
def getHeaderImg(img1, img2):
    # 先頭から1行ずつ比較し、不一致となるまでをヘッダとみなす
    headerImg = 0
    imgH = img1.shape[SHAPE_HEIGHT]
    for height in range(1, imgH):
        img1Cmp = img1[0:height]
        img2Cmp = img2[0:height]
        matchRate = getMatchRate(img1Cmp, img2Cmp, img1Cmp.size)
        if 100 * 10 != matchRate:
            headerImg = img1Cmp
            break

    return headerImg


# キャプチャした画像のうち、2枚の画像に共通する部分をフッターとして取得する
# Warning：同じサイズのimgを2つ指定すること
# 入力1：共通部分を取得したい画像のimg1
# 入力2：共通部分を取得したい画像のimg2
# 出力：フッターに相当するimg
def getFooterImg(img1, img2):
    # 末尾から1行ずつ比較し、不一致となるまでをヘッダとみなす
    footerImg = 0
    imgH = img1.shape[SHAPE_HEIGHT]
    for height in range(1, imgH):
        startPos = imgH - height
        img1Cmp = img1[startPos:imgH]
        img2Cmp = img2[startPos:imgH]
        matchRate = getMatchRate(img1Cmp, img2Cmp, img1Cmp.size)
        if 100 * 10 != matchRate:
            footerImg = img1Cmp
            break

    return footerImg


# キャプチャした画像のうち、2枚の画像に共通する部分を左カラムとして取得する
# Warning：同じサイズのimgを2つ指定すること
# 入力1：共通部分を取得したい画像のimg1
# 入力2：共通部分を取得したい画像のimg2
# 出力：左カラムに相当するimg
def getColumnLImg(img1, img2):
    # 末尾から1行ずつ比較し、不一致となるまでをヘッダとみなす
    columnLImg = 0
    imgW = img1.shape[SHAPE_WIDTH]
    for width in range(1, imgW):
        img1Cmp = img1[:, 0:width]
        img2Cmp = img2[:, 0:width]
        matchRate = getMatchRate(img1Cmp, img2Cmp, img1Cmp.size)
        if 100 * 10 != matchRate:
            columnLImg = img1Cmp
            break

    return columnLImg


# キャプチャした画像のうち、2枚の画像に共通する部分を右カラムとして取得する
# Warning：同じサイズのimgを2つ指定すること
# 入力1：共通部分を取得したい画像のimg1
# 入力2：共通部分を取得したい画像のimg2
# 出力：右カラムに相当するimg
def getColumnRImg(img1, img2):
    # 末尾から1行ずつ比較し、不一致となるまでをヘッダとみなす
    columnRImg = 0
    imgW = img1.shape[SHAPE_WIDTH]
    for width in range(1, imgW):
        startPos = imgW - width
        img1Cmp = img1[:, startPos:imgW]
        img2Cmp = img2[:, startPos:imgW]
        matchRate = getMatchRate(img1Cmp, img2Cmp, img1Cmp.size)
        if 100 * 10 != matchRate:
            columnRImg = img1Cmp
            break

    return columnRImg


# 指定数の画像を読み込んでリストとして返す
# 入力：読み込みたい画像数
# 入力：トリミングしたい部位のサイズ(ヘッダ、フッタ、左カラム、右カラム)
def getImgLst(imgCnt_r, trim_r):
    imgLst = []
    for cnt in range(imgCnt_r):
        # 画像を読み込む
        imgName = genOutPutFileName(cnt)
        rdImg = cv2.imread(imgName)

        # ヘッダー部分をトリミングする
        if 0 < trim_r[0]:
            imgH = rdImg.shape[SHAPE_HEIGHT]
            imgTrmHead = rdImg[trim_r[0]:imgH]
        else:
            imgTrmHead = rdImg

        # 末尾以外のウィンドウ下部をきりとる
        imgH = imgTrmHead.shape[SHAPE_HEIGHT]
        if (imgCnt_r - 1) > cnt:
            # フッター部分をトリミングする
            if 0 < trim_r[1]:
                endPos = imgH - trim_r[1]
            else:
                # Windows11ならではというよりは、テーマ次第？
                # 四隅がラウンドになっている部分をカットしたい
                endPos = imgH - 10
        else:
            endPos = imgH
        imgTrmFoot = imgTrmHead[0:endPos]

        # 左カラム部分をトリミングする
        if 0 < trim_r[2]:
            imgW = imgTrmFoot.shape[SHAPE_WIDTH]
            imgTrmColL = imgTrmFoot[:, trim_r[2]:imgW]
        else:
            imgTrmColL = imgTrmFoot

        # 右カラム部分をトリミングする
        if 0 < trim_r[3]:
            imgW = imgTrmColL.shape[SHAPE_WIDTH]
            endPos = imgW - trim_r[3]
            imgTrmColR = imgTrmColL[:, 0:endPos]
        else:
            imgTrmColR = imgTrmColL

        # トリミングした状態のimgをリスト化する
        imgLst.append(imgTrmColR)

    return imgLst


# 画像を結合する
# note：画像を垂直シフトしながら重複箇所を探して結合する
# waring：背景に画像があると一致率の判定に上手くいかない
# 入力：結合したい画像のリスト
# 出力：結合した画像のImg
def getStitchImg(imgLst_r):
    pageCnt = len(imgLst_r)
    stitcImg = imgLst_r[0]
    for page in range(1, pageCnt):
        rdImg = imgLst_r[page]
        rdImgH = rdImg.shape[SHAPE_HEIGHT]
        sticImgH = stitcImg.shape[SHAPE_HEIGHT]

        # 2つの画像サイズを合わせる
        if rdImgH < sticImgH:
            # 結合される側のサイズが大きい場合
            # (上部側の方が重複している部分は少ないと考えられるため、結合される側の画像上部をトリミングする)
            trmStart = sticImgH-rdImgH
            sticImgAdj = stitcImg[trmStart:sticImgH]
            rdImgAdj = rdImg
        elif rdImgH > sticImgH:
            # 結合する側のサイズが大きい場合
            # (下部側の方が重複している部分は少ないと考えられるため、結合する側の画像下部をトリミングする)
            trmEnd = sticImgH
            rdImgAdj = rdImg[0:trmEnd]
            sticImgAdj = stitcImg
        else:
            # 画像サイズが一致するなら何もしない
            sticImgAdj = stitcImg
            rdImgAdj = rdImg

        # 順番に結合する
        maxRate = 0
        trmPosStart = 0
        sticImgAdjH = sticImgAdj.shape[SHAPE_HEIGHT]
        rdImgAdjH = rdImgAdj.shape[SHAPE_HEIGHT]
        for cntH in range(rdImgAdjH):
            # 結合される側は先頭からトリミングする
            cmpImgTrm = sticImgAdj[cntH:sticImgAdjH]
            # 結合する側は末尾からトリミングする
            rdImgEnd = rdImgAdjH - cntH
            rdImgTrm = rdImgAdj[0:rdImgEnd]

            # サイズの大きい方で一致率を算出する
            if rdImgTrm.size > cmpImgTrm.size:
                baseSize = rdImgTrm.size
            else:
                baseSize = cmpImgTrm.size

            # 最も重複するトリミング位置を決定する
            matchRate = getMatchRate(cmpImgTrm, rdImgTrm, baseSize)
            if maxRate < matchRate:
                maxRate = matchRate
                trmPosStart = cntH

        startPos = rdImgAdjH - trmPosStart
        rdImgTrm = rdImgAdj[startPos:rdImgAdjH]
        stitcImg = cv2.vconcat([stitcImg, rdImgTrm])
        print("結合数: " + str(page) + "/" + str(pageCnt-1))

    return stitcImg


# ウィンドウ内のページ全体をキャプチャする
# 入力1:キャプチャした結果の保存先(パス+ファイル名+拡張子)
def captureWindow(savePath_r):
    pageCnt = getPageImg()

    # 重複部分をトリミングする
    if 2 <= pageCnt:
        # ファイル名を取得する
        img1Name = genOutPutFileName(0)
        img2Name = genOutPutFileName(1)
        # ファイルを読み込む
        img1 = cv2.imread(img1Name)
        img2 = cv2.imread(img2Name)

        # ヘッダーを削除する
        headImg = getHeaderImg(img1, img2)
        headImgH = headImg.shape[SHAPE_HEIGHT]

        # フッターを削除する
        footerImg = getFooterImg(img1, img2)
        footerImgH = footerImg.shape[SHAPE_HEIGHT]

        # 左カラムを削除する
        colL = getColumnLImg(img1, img2)
        colLW = colL.shape[SHAPE_WIDTH]

        # 右カラムを削除する
        colR = getColumnRImg(img1, img2)
        colRW = colR.shape[SHAPE_WIDTH]
    else:
        headImgH = 0
        footerImgH = 0
        colLW = 0
        colRW = 0

    trimSiz = (headImgH, footerImgH, colLW, colRW)
    # キャプチャした画像を結合できる状態にする
    imgLst = getImgLst(pageCnt, trimSiz)

    # キャプチャした画像を結合する
    stitcImg = getStitchImg(imgLst)

    cv2.imwrite(savePath_r, stitcImg)


def main():
    savePath = OUTPUT_PATH + OUTPUT_NAME_UNION + OUTPUT_EXT
    captureWindow(savePath)


if __name__ == "__main__":
    main()

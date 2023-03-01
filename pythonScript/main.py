import dispCapt
import convImg2Str


def main():
    savePath = r"\\wsl.localhost\Ubuntu\home\okome\ocrTesseract\work\src\image.jpg"
    dispCapt.captureWindow(savePath)
    convImg2Str.execConvert()


if __name__ == "__main__":
    main()

import subprocess


# WSL2上のdockerコンテナで変換を実行する
def execConvert():
    # PowerShellコマンドを構築
    exeCmd = 'powershell.exe'
    cmdCmd = '-Command'

    # rootユーザでUbuntuを起動
    wakeupWSL = 'wsl -d Ubuntu -u root'
    # Ubuntu内でbashを起動
    startBash = '/bin/bash'
    # bash上でdockerデーモン起動・ディレクトリ移動・コンテナ起動
    bashCmd = '-c "service docker start & cd /home/okome/ocrTesseract/ && docker compose up"'
    # コマンドを結合
    mainCmd = wakeupWSL + ' -- ' + startBash + ' ' + bashCmd

    # PowerShellに与えるコマンドを用意
    cmdLst = [
        exeCmd,
        cmdCmd,
        mainCmd
    ]

    # サブプロセスとしてコマンドを実行
    subprocess.run(cmdLst)


def main():
    execConvert()


if __name__ == "__main__":
    main()

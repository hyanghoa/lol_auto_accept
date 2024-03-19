# lol_auto_accept

롤 매칭 자동 수락 프로그램입니다.

### env (가상환경)

개발을 위한 가상환경 설치

```bash
pip install -r requirements.txt
```

### 실행 파일 만들기

pyinstaller를 사용한 exe 실행 파일을 만드려면 아래 명령어를 입력

```bash
pyinstaller --onefile --noconsole --add-data accept_button.png:. --name lol_auto_accept tk.py
```

### 실행 화면

<img width="480" src="./readme/images/run_sample.png" alt="run example">
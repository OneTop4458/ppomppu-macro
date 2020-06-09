# 뽐뿌 매크로
> 뽐쿠폰 획득을 위한 자동 댓글 매크로 입니다.

## 사용 방법
1. `git clone https://github.com/OneTop4458/ppomppu-macro.git`
> 오른쪽 중반 Clone or download 버튼 클릭 > Download Zip을 클릭하여 다운로드 하는 방법도 가능합니다.
2. `압축 해제`
3. `python-3.8.0.exe 설치`
> ※ 설치 시 하단 Add Python 3.8 to PATH 체크
4. `Win + R 키 입력 후 CMD 입력`
5. `pip install selenium 입력`
6. `Chrome 다운로드`
7. `Chrome 실행 후 오른쪽 상단 ... 클릭>도움말(E)>Chrome 정보(G) 클릭 후 Chrome 버전 확인`
8. `https://chromedriver.chromium.org/downloads 에서 자신의 버전과 맞는 Chrome Driver 다운로드`
> ※ Chrome 버전과 Chrome Driver 버전 상이시 에러 발생
9. `다운로드 한 chromedriver.exe 를 매크로가 있는 디렉터리에 복사`
10. `https://www.base64encode.org 에서 자신의 뽐뿌 아이디, 비밀번호 Base64 인코딩`
11. `config.json 파일에 Base64로 인코딩된 자신의 뽐뿌 아이디, 비밀번호 입력`
> ※ otp 로그인 설정 시 매크로 사용 불가
12. `스크립트 실행`
> run_macro.py

### 주의 사항
1. python-3.8.0.exe 설치 시 설치시 하단 Add Python 3.8 to PATH 체크
2. Chrome 버전과 Chrome Driver 버전 상이시 에러발생
3. otp 로그인 설정시 매크로 사용 불가
4. config_comment.txt 저장시 BOM 없는 UTF-8로 저장해야함
> config_comment.txt는 매크로가 입력할 댓글을 지정할 수 있음

## 기여하기
버그 등이 발생하면 이슈로 등록해 주시거나, 문제가 되는 부분을 수정하신 후 PR해 주시면 감사하겠습니다.

## 라이선스
이 매크로는 [MIT 라이선스](https://github.com/OneTop4458/ppomppu-macro/blob/master/LICENSE)를 적용받습니다.


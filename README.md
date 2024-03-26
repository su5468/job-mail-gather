# Job Mailing Gathering

바람과 같이 지나가는 취업 시즌에, 구직 플랫폼의 메일링 서비스를 한번에 모아서 볼 수 있다면 얼마나 좋을까요.  
Job Mailing Gathering은 여러 구직 플랫폼의 구인 메일링 서비스를 취합하여, 한번에 보여줍니다.

## 시작하기

1. 각 플랫폼의 메일링 서비스를 받을 메일 계정을 준비합니다.
2. 해당 메일 계정의 IMAP 설정을 활성화합니다.
    - Gmail을 사용하는 경우, [구글 계정 보안 설정](https://myaccount.google.com/security)에서 2단계 인증을 활성화하고, *앱 비밀번호*를 설정하고 복사해둡니다.
3. 취업 플랫폼별 메일링 서비스를 등록합니다.
4. `config.ini` 파일에서 내가 사용하는 메일 계정을 `service` 섹션의 `name`에 설정합니다.
    - 현재 가능한 값은 `gmail` 입니다.
5. `account.ini` 파일에서 해당 메일 섹션에 `id`와 `pw`를 설정합니다.
    - Gmail을 사용하는 경우, `pw`는 구글 비밀번호가 **아니라**, 조금 전 설정한 *앱 비밀번호*입니다.
6. `main.py`를 실행하면, 지난 이틀간 수신한 메일링 서비스의 직무들을 정리해서 보여줍니다.

## 지원 플랫폼

-   링크드인
-   사람인 (WIP)
-   잡코리아 (WIP)
-   잡플래닛 (WIP)
-   점핏 (WIP)
-   원티드 (WIP)
-   블라인드 하이어 (WIP)

## 컨피그 설정하기

-   **service**: 사용하는 메일 계정과 관련된 설정입니다.
    -   **name**: 메일 서비스 종류입니다. 현재 `gmail`만 지원이 보장됩니다.
    -   **mailbox**: 메일링 서비스의 메일이 수신되는 사서함 이름입니다. 기본값은 `INBOX`고, 잘 모르겠다면 바꾸지 마십시오.
-   **config**: 일반 설정입니다.
    -   **recent_days**: 최근 며칠의 메일을 가져올지에 관한 설정입니다. 기본값은 이틀입니다.
-   **from.플랫폼이름**: `from.`으로 시작하는 섹션은 해당 메일링 서비스의 메일을 가져오는데 필요한 값들입니다.
    -   **address**: 메일링 서비스의 송신자입니다.
    -   **subject**: 메일링 서비스의 제목에 들어가는 문자열입니다.

## 추가하기

아래 방법으로 여러 개의 메일 계정에 수신하고 있는 메일링 서비스를 모아볼 수 있습니다.

1. `account.ini`에 새로운 섹션을 생성합니다.
2. `config.ini`의 `service` 섹션, `name`의 값을 `account.ini`에 있는 섹션 이름과 일치시킵니다.

## TODO

-   [ ] 추가: 사람인
-   [ ] 추가: 잡코리아
-   [ ] 추가: 잡플래닛
-   [ ] 추가: 점핏
-   [ ] 추가: 원티드
-   [ ] 추가: 블라인드 하이어
-   [ ] 결과를 html로 정리하여 보여주기

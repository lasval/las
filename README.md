# Quick summary #
이 레포지토리는 Docker를 이용한 Django 프로젝트의 스타터 킷 예시 입니다.
> Production모드에서는 nginx + gunicorn을 사용하고, Dev모드에서는 django 개발용 서버를 사용 합니다.


-----




# How do I get set up? #
Docker 관련 설치 가이드들은 Notion에서도 확인하실 수 있습니다.
[Notion 개발 설치 가이드 모음](https://www.notion.so/3c87d75afd5348e5b1b90cc5b0e14a00)

## Docker 설치 ##

> Ubuntu에 설치한다고 가정 (가이드 작성 당시 Ubuntu 20.04.1 LTS 버전)

### Docker 설치 및 기본 설정 ###

**Docker가 설치되어 있지 않다면 아래 명령어를 통해 Docker 설치**

```bash
$ curl -fsSL https://get.docker.com/ | sudo sh
```

**sudo 없이 사용하기**

docker는 기본적으로 root권한이 필요합니다. root가 아닌 사용자가 sudo없이 사용하려면 해당 사용자를 `docker`그룹에 추가합니다.

```bash
$ sudo usermod -aG docker $USER # 현재 접속중인 사용자에게 권한주기
$ sudo usermod -aG docker your-user # your-user 사용자에게 권한주기
```

### Docker compose 설치 ###

아래 명령어를 통해 docker compose설정 버전을 바꾸고 싶으면 1.27.4 부분을 바꾸면 됨

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

권한 설정

```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```

버전확인 명령어로 docker compose 정상 설치 확인

```bash
$ docker-compose --version
```

docker compose 설치 관련 문제가 생기면 도커 공식 홈페이지 참조

[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)


-----




## .env파일 해당 프로젝트 Root Directory에 저장 (.env.prod & .env.dev) ##

<.env.prod 파일 형태>

```bash
DEBUG=0
SECRET_KEY=시크릿키입력
DJANGO_ALLOWED_HOSTS=Django에서 Allow Host로 사용할 값들 (띄어쓰기로 구분하여 작성, ex: 11.11.11.11 localhost [::1])
DB_ENGINE=django.db.backends.postgresql (postgreSQL 사용 예시)
DB_NAME=Production용 DB명
DB_USER=Production용 DB에 접속할 유저명
DB_PASSWORD=Production용 DB에 접속할 유저의 비밀번호
DB_HOST=Production용 DB Host주소
DB_PORT=Production용 DB 포트
```

<.env.dev 파일 형태>

```bash
DEBUG=1
SECRET_KEY=시크릿키입력
DJANGO_ALLOWED_HOSTS=* (Dev 모드에서는 모두 허용해주기 위해 *를 지정)
DB_ENGINE=django.db.backends.postgresql (postgreSQL 사용 예시)
DB_NAME=QA or DEV용 DB명
DB_USER=QA or DEV용 DB에 접속할 유저명
DB_PASSWORD=QA or DEV용 DB에 접속할 유저의 비밀번호
DB_HOST=QA or DEV용 DB Host주소
DB_PORT=QA or DEV용 DB 포트
```

<.env.dev 파일 **예시**>

```bash
DEBUG=1
SECRET_KEY=a@$SDF-secret-key-for-qa
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=test_db
DB_USER=test_db_admin
DB_PASSWORD=admin_password
DB_HOST=db.devdb.com
DB_PORT=5432
```


-----




## docker 명령어를 이용한 실행 ##
Production 모드로 이미지 생성 및 실행: 

```bash
$ docker-compose up -d --build 
```

Dev 모드로 이미지 생성 및 실행: 

```bash
$ docker-compose -f docker-compose-dev.yml up --build
```


------




[Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)







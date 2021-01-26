# README #

This README would normally document whatever steps are necessary to get your application up and running.

------

## Quick summary ##
이 레포지토리는 Docker를 이용한 Django 프로젝트의 스타터 킷 예시 입니다.

## How do I get set up? ##

#### Docker 설치 ####
.env파일 해당 프로젝트 Root Directory에 저장 (.env.prod & .env.dev)

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


#### docker 명령어를 이용한 실행 ####
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
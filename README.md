# Quick summary #
이 레포지토리는 Docker를 이용한 Django 프로젝트의 스타터 킷 예시 입니다.
Production모드에서는 nginx + gunicorn을 사용하고, Dev모드에서는 django 개발용 서버를 사용 합니다.


-----

# 기본 디렉토리 구조 및 설명 #
Docker Compose를 이용하여 한번에 django 컨테이너와 nginx 컨테이너를 실행하고 연결시켜주기 위해
아래와 같은 구조로 디렉토리를 구성함

**기본 디렉토리 구조 (숨김파일 제외)**
```bash
├── django
├── nginx
├── README.md
├── docker-compose-dev.yml
└── docker-compose.yml
```

**기본 디렉토리 구조 (숨김파일 포함)**
```bash
├── .git
├── django
├── nginx
├── .env.dev
├── .env.prod
├── .gitignore
├── README.md
├── docker-compose-dev.yml
└── docker-compose.yml
```

**각 디렉토리 및 파일 설명**

- .git: 깃 디렉토리
- django: Django 프로젝트가 담긴 디렉토리 
(Dockerize를 위해 해당 디렉토리 내부에 `Dockerfile`과 `requirements.txt`를 추가함)
- nginx: Production모드로 django 프로젝트 컨테이너를 실행할 때 사용하는 nginx 관련 디렉토리
(Dockerize를 위한 nginx `Dockerfile`과 nginx 설정파일인 `nginx.conf`가 포함된 디렉토리)
- .env.dev: Dev 모드로 빌드/실행할 때 참조하는 env파일 (Django내에서 사용하는 설정 값)
- .env.prod: Production 모드로 빌드/실행할 때 참조하는 env파일 (Django내에서 사용하는 설정 값)
- .gitignore: gitignore파일 (django/nginx 디렉토리 상위에 있기 때문에 django관련 파일을 무시하기 위해 /django/static과 같이 표현해줌)
- README.md: git 저장소 (bitbucket)에서 보여지는 README markdown 파일
(프로젝트 관련 설명 포함)
- docker-compose-dev.yml: Dev 모드로 빌드/실행할 때 사용하는 `docker-compose`파일
    - 실행 예시: $ docker-compose -f docker-compose-dev.yml up —build
- docker-compose.yml: Production 모드로 빌드/실행할 때 사용하는 `docker-compose`파일
    - 실행 예시: $ docker-compose up -d —build
    - docker-compose.yml은 docker-compose기본 파일이므로 따로 명령어에서 지정해주지 않아도 됨



# 실행/개발 전 사전 준비사항 #
Docker 관련 설치 가이드들은 Notion에서도 확인하실 수 있습니다.
[Notion 개발 설치 가이드 모음](https://www.notion.so/3c87d75afd5348e5b1b90cc5b0e14a00)

## **1. Docker 설치** ##
Ubuntu에 설치한다고 가정 (가이드 작성 당시 Ubuntu 20.04.1 LTS 버전)

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


## **2. Git을 통해 해당 프로젝트 다운** ##
git clone https://해당 프로젝트 접근 가능한 빗버킷 계정@bitbucket.org/gymt-tonline/docker-on-django-starter-kit.git

-----




## **3. 필요한 환경변수 파일 생성 및 저장(.env.prod & .env.dev & /django/.env)** ##

.env.prod: Docker Compose를 사용할 때 Production 모드의 환경변수로 사용할 파일

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

.env.dev: Docker Compose를 사용할 때 Dev 모드의 환경변수로 사용할 파일

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

/django/.env: docker를 사용하지 않고 pipenv환경내에서 runserver로 실행할 때 필요한 파일 (.env.dev파일과 동일)

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


.env.dev 파일 **예시**

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




# **Docker 명령어를 이용한 실행** #
## **Production 모드로 이미지 생성 및 실행:** ##

Production 모드는 소스코드와 static 파일들을 컨테이너에 복사하고 독립적으로 실행한다.

따라서, 실행전 필요하다면 아래 명령어들을 선행적으로 실행해주어야 해당 사항이 반영된다.

(참고로 django 관련 명령어는 pipenv등의 로컬의 가상환경내에서 실행하는 것을 권장한다. *아래 쉘 명령어 입력 예시에서 앞의 (django)부분은 pipenv 가상환경임을 의미)

(Docker Compose 빌드/실행 이전에) `makemigrations`과 `migrate` 명령어는 필요시에 실행한다.

```bash
(django) $ python manage.py makemigrations
```

```bash
(django) $ python manage.py migrate
```

Producntion 모드로 빌드/실행하기 전에 `collectstatic`은 필수로 실행해주는 것을 권장한다.
```bash
(django) $ python manage.py collectstatic
```

프로젝트 root 디렉토리에서 아래 명령어를 실행

```bash
$ docker-compose up -d --build 
```

명령어 관련 설명

- `up`: Docker Compose(`docker-compose.yml` 파일)에 정의된 모든 서비스 컨테이너들을 한 번에 생성하고 실행하기 위한 명령어. 단, 해당 명령어에 `--build` 옵션을 명시해주지 않으면 변경사항이 반영되지 않음
- `-d` 옵션: detached 모드로써 백그라운드로 실행하여 로그가 보이지 않도록 함
- `--build`: 명시적으로 이미지를 새로 빌드하는 옵션. 프로젝트 코드에 변경사항이 있을 경우 해당 옵션을 명시해줘야만 반영됨


## **Dev 모드로 이미지 생성 및 실행:** ##

프로젝트 root 디렉토리에서 아래 명령어를 실행

```bash
$ docker-compose -f docker-compose-dev.yml up --build
```

명령어 관련 설명

- `up`: Production 모드와 동일
- `--build`: Production 모드와 동일
- `-f`: docker-compose-dev.yml파일을 통해 빌드/실행하기 위한 옵션 (해당 옵션을 지정하지 않으면 docker-compose.yml파일을 참조하여 빌드/실행됨)
- 참고사항(1): Dev 모드로써 서버 로그를 실시간으로 확인하기 위해서 -d 옵션은 주지 않음
- 참고사항(2): Dev 모드에서는 코드 변경을 실시간으로 반영하기 위해 django 디렉토리 하위의 `Dockerfile-dev`파일에 정의된 값들을 통해 로컬의 소스코드를 컨테이너와 바인딩 시킴


### **Production or Dev 모드로 빌드/실행할 때 주의해야할 점** ###

`--build` 옵션을 통해 Production 모드나 Dev 모드로 컨테이너를 실행할 때 코드 상에 변경사항이 있으면 새로운 이미지가 만들어지게 된다. 

코드 변경 전 이미지

```bash
$ docker images
REPOSITORY           TAG            IMAGE ID       CREATED         SIZE
tonline/django       latest         bcd85ffe3187   8 minutes ago   647MB
tonline/django-dev   latest         7121aaf87ebe   3 hours ago     647MB
tonline/nginx        latest         ba7b66ec5f59   22 hours ago    22.3MB
```

코드 변경 후 새로 실행 (docker-compose up -d --build)

```bash
$ docker images
REPOSITORY           TAG            IMAGE ID       CREATED          SIZE
tonline/django       latest         66390b847cf4   48 seconds ago   647MB
<none>               <none>         bcd85ffe3187   9 minutes ago    647MB
tonline/django-dev   latest         7121aaf87ebe   3 hours ago      647MB
tonline/nginx        latest         ba7b66ec5f59   22 hours ago     22.3MB
```

위의 예시에서 볼 수 있듯이 소스코드를 변경하여 다시 컨테이너를 실행하면 새로운 이미지가 만들어져 66390b847cf4라는 새로운 IMAGE ID를 갖게 되고
기존의 bcd85ffe3187 IMAGE ID를 가진 이미지는 `<none>`으로 표시된다.

**위와 같이 `docker images` 명령어에서 `<none>`:`<none>`으로 보여지는 이미지들은 dangling 이미지로써 불필요한 디스크 용량을 차지할 수 있으므로 주기적으로 삭제해주는 것이 좋다.**
(단, `docker images -a`명령어를 통해서만 보여지는 `<none>`:`<none>`은 기존 이미지 레이어의 child 이미지로 용량 문제가 없다.)

사용하지 않고 dangling된 이미지만 명확히 찾기 위해 아래 명령어를 사용할 수도 있다.

```bash
$ docker images -f "dangling=true" -q
10a955570057 <--dangling된 이미지 ID를 리턴한다.
```

이와 같은 dangling된 이미지는 docker rmi명령어를 통해 삭제하면 된다.

```bash
$ docker rmi 10a955570057
```


## **Docker를 사용하지 않고 가상환경으로 실행 (pipenv & runserver)** ##

django 프로젝트 부분은 pipenv를 사용한 python 가상환경을 기준으로 작성되었음.

`makemigrations`, `migrate`, `collectstatic` 명령어들을 실행하기 위해서는 현재 상태에서는 pipenv를 이용한 가상환경 상태에서 실행해야함

pipenv 를 이용한 가상환경 활성화 명령어

```bash
$ pipenv shell
Loading .env environment variables...
Launching subshell in virtual environment...
 . /Users/example/.local/share/virtualenvs/django-DAeX99bh/bin/activate
➜  django git:(master) ✗  . /Users/example/.local/share/virtualenvs/django-DAeX99bh/bin/activate
(django) $  <-- 가상환경 활성화되면 쉘 앞에 (django)가 붙는다
```

docker를 사용하지 않고 pipenv 가상환경을 활성화한 상태에서 로컬 서버를 실행하고 싶을 때에는 아래의 명령어를 사용하면 된다.

```bash
(django) $ python manage.py runserver
```



Docker on Django 관련 자세한 가이드(추가로 알아야하는 명령어 포함)는 Notion을 통해서도 확인가능합니다.
[Docker on Django 관련 가이드](https://www.notion.so/Docker-on-Django-a051d1df294c47a1b4886fba2d276dd5)

------




[Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)







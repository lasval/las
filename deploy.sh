#!/bin/bash
 
# Blue 를 기준으로 현재 떠있는 컨테이너를 체크한다.
EXIST_BLUE=$(docker-compose -p docker -f docker-compose-blue.yml ps | grep Up | grep las-django-blue1)
 
# 컨테이너 스위칭
if [ -z "$EXIST_BLUE" ]; then
    echo "blue up"
    docker-compose -p docker -f docker-compose-blue.yml up -d
    BEFORE_COMPOSE_COLOR="green"
    AFTER_COMPOSE_COLOR="blue"
else
    echo "green up"
    docker-compose -p docker -f docker-compose-green.yml up -d
    BEFORE_COMPOSE_COLOR="blue"
    AFTER_COMPOSE_COLOR="green"
fi
 
sleep 10
 
# 새로운 컨테이너가 제대로 떴는지 확인
EXIST_AFTER=$(docker-compose -p docker -f docker-compose-${AFTER_COMPOSE_COLOR}.yml ps | grep Up | grep las-django-${AFTER_COMPOSE_COLOR}1)
if [ -n "$EXIST_AFTER" ]; then
    # conf.d 수정후 리로드 
    docker exec -ti las-nginx-${AFTER_COMPOSE_COLOR} sh -c "cp /etc/nginx/nginx-${AFTER_COMPOSE_COLOR}.conf /etc/nginx/conf.d/nginx.conf"
    docker exec -it las-nginx-${AFTER_COMPOSE_COLOR} nginx -s reload
    echo "nginx reload"
    # 이전 컨테이너 종료
    docker-compose -f docker-compose-${BEFORE_COMPOSE_COLOR}.yml down
    echo "$BEFORE_COMPOSE_COLOR down"
fi
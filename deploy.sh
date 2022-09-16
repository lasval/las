#!/bin/bash
 
# Blue 를 기준으로 현재 떠있는 컨테이너를 체크한다.
EXIST_BLUE=$(docker-compose -p docker_web1-blue -f docker-compose.blue.yaml ps | grep Up)
 
# 컨테이너 스위칭
if [ -z "$EXIST_BLUE" ]; then
    echo "blue up"
    docker-compose -p docker_web1-blue -f docker-compose.blue.yaml up -d
    BEFORE_COMPOSE_COLOR="green"
    AFTER_COMPOSE_COLOR="blue"
else
    echo "green up"
    docker-compose -p docker_web1-green -f docker-compose.green.yaml up -d
    BEFORE_COMPOSE_COLOR="blue"
    AFTER_COMPOSE_COLOR="green"
fi
 
sleep 10
 
# 새로운 컨테이너가 제대로 떴는지 확인
EXIST_AFTER=$(docker-compose -p docker_web1-green -f docker-compose.green.yaml ps | grep Up)
if [ -n "$EXIST_AFTER" ]; then
    # 이전 컨테이너 종료
    docker-compose -p docker_web1-blue -f docker-compose.blue.yaml down
    echo "blue down"
fi
#!/bin/bash

read -p '영문 소문자로 프로젝트 명을 입력해주세요(ex. parkpro): ' projectname

{
    mv django/parkpro_api django/${projectname}_api && find ./ -type f -exec sed -i '' "s/parkpro/${projectname}/g" {} \; 
} || {
    echo "파일명 변경은 최초 1회만 하시기 바랍니다."
}

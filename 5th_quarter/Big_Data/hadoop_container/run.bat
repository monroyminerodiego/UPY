@echo off
set IMAGE_NAME=hadoop-docker
set CONTAINER_NAME=hadoop-container

echo Building Docker image...
docker build -t %IMAGE_NAME% .

echo Checking if container is already running...
docker ps --filter "name=%CONTAINER_NAME%" --format "{{.Names}}" | findstr /r "^%CONTAINER_NAME%$" > nul
if %ERRORLEVEL% == 0 (
    echo Container %CONTAINER_NAME% is already running.
) else (
    echo Container is not running, starting a new one...
    docker run -d --name %CONTAINER_NAME% ^
    -p 9870:9870 ^
    -p 9864:9864 ^
    -p 8042:8042 ^
    -p 8088:8088 ^
    -p 10020:10020 ^
    -p 19888:19888 ^
    %IMAGE_NAME%
    echo Container %CONTAINER_NAME% has been started.
)

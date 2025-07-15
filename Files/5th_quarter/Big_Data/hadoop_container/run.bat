@echo off
cls
set IMAGE_NAME=hadoop-docker
set CONTAINER_NAME=hadoop-container

echo Building Docker image...
docker build -t %IMAGE_NAME% .

echo Deleting existing container...
docker rm -f %CONTAINER_NAME%


echo Starting a new container...
@REM docker run -d -P --name %CONTAINER_NAME% %IMAGE_NAME%
docker run -it --name %CONTAINER_NAME% ^
-p 8088:8088 ^
-p 8042:8042 ^
-p 50070:50070 ^
-p 50075:50075 ^
-p 50010:50010 ^
-p 50020:50020 ^
-p 50090:50090 ^
%IMAGE_NAME%



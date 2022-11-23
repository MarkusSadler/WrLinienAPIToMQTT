git pull

docker build -t wrlinientomqqtt:$1 .
docker stop wrlinientomqqtt
docker rm wrlinientomqqtt
docker run --rm -d --name wrLininenToMqtt wrlinientomqqtt:$1

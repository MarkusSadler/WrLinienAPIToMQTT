git pull

docker build -t wrlinientomqqtt:$1 .
docker stop wrLininenToMqtt
docker rm wrLininenToMqtt
docker run -d --restart unless-stopped --name wrLininenToMqtt wrlinientomqqtt:$1

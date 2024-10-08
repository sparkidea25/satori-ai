Satori AI knowledge base application

python3 -m venv env

create .env
add OPEN_API_KEY = 

docker build -t satori-ai --platform linux/amd64 .
docker images
docker tag 4634b91882ef serversidea/model-test
docker push serversidea/model-test
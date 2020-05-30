docker container stop $(docker container ls -aq)
docker container rm $(docker container ls -aq)

docker image rm asmi-clothing-api:1.0.0
docker build -t asmi-clothing-api:1.0.0 .
docker run -p 4000:4000 -d --name asmi-api asmi-clothing-api:1.0.0

docker container ps
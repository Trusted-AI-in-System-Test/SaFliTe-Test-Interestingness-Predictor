# As ROOT
cd /home/engineer/Aerialist

git pull

docker container kill $(docker ps -q)
docker container prune -f

docker rmi -f skhatiri/aerialist:latest
docker build --no-cache . -t skhatiri/aerialist

cd /home/engineer/Aerialist_Test_Generator/snippets
source /usr/local/bin/.venv/bin/activate
python random_generator.py
####Instalando Docker
# 1º   sudo apt-get remove docker docker-engine docker.io containerd runc
# 2º   sudo apt-get update
# 3º   sudo apt-get install \
#      ca-certificates \
#      curl \
#      gnupg \
#      lsb-release
# 4º   sudo mkdir -p /etc/apt/keyrings
# 5º   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# 6º   echo \
#      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# 7º   sudo apt-get update
# 8º   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
# 9º   sudo usermod -aG docker $USER  
# 10º  reinicia o pc

docker run "nome" #roda o docker, caso não tiver, baixa e roda

docker pull "nome" #baixa o docker

docker ps          #mostra os dockers rodando atualmente

docker ps -a       #mostra todos os dockers rodados

docker strop "nome" #para um docker, deixando ele em estado de "parado"

docker start "nome" #roda o docker que esta "parado"

docker exec -it "id" "comando" #executa o comando dentro do docker

docker pause "nome" #pausa o docker

docker unpause "nome" #despausa o docker

docker run -it "imagem" "comando" #roda o docker de forma iterativa

docker run -d -p 8080:80 "nome" #roda o docker mudando a porta 80 do docker para ser equivalente a porta 8080

docker inspect "nome" #mostra informações do container

docker history "imageid" #mostra as camadas da imagem

docker build -t "nome":"versao" "diretorio"

docker stop $(docker container ls -q) #para todos os docker em execucao
####Cadastrar um usuario git
# 1º ssh-keygen -t ed25519 -C email@gmail.com
# 2º na pasta de usuario -> cd .ssh/ -> cat id_ed255519.pub
# 3º copiar a key e colar em 'https://github.com/settings/keys'
# 4º git config --global user.email "seu nome"
# 5º git config --global user.name  "seu email"

git init #inicia um repositorio
git init --bare #inicia repositorio "servidor"

git status #mostra status do repositorio atual

git add arquivo.txt #adicionar arquivo para o git monitorar

git add . #adicionar todos os arquivos da pagina atual

git rm --cached arquivo.txt #para remover arquivo do monitoramento do git

git commit -m ?"mensagem de commit" #Adiciona arquivos q estão monitorados pelo git a lista de commits

git remote #lista todos repositorios remotos registrado
git remote -v #mostra local com caminho e versão
git remote add "nome" "endereco" #adiciona um repositorio remoto
git remote rename "nomeatual" "novonome" #renomeia repositorio

git clone "caminho" "nome" #clona repositorio salvo no endereço (ps: endereço pode ser link do github ex: https://github.com/Bloo5/Name_Origin.git)

git push "local" "branch" #sobe as mudanças git para o repositorio

git pull "nome" "branch" #pega os dados do repositorio

git checkout -- arquivo.txt #retorna o arquivo para a versão anterior caso não tenha sido adicionado

git reset "branch" arquivo.txt #reseta o arquivo do branch, assim removendo ele do "add"
###### git branch ######
git branch # mostra as branchs
git branch "nome" #cria branch com novo nome
git checkout "nomebranch" #muda a branch
git merge "nome" #puxa as informações de outra branch
git rebase "nome" #puxa os commit da branch atual e junta com os commit da branch especificada 

###### git .gitignore ######
#1º cria arquivo .gitignore
#2º git add .gitignore
#3º git commit .gitignore
pasta/ #ignora pasta e todos seus arquivos
.log #ignora todos os arquivos q terminar com .log

###### git log ######
git log #mostra historico de commits
git log --oneline #mostra tudo em uma linha
git log -p #mostra as alterações dos commits
#https://devhints.io/git-log

###### git config ######
git config --local #muda configurações do repositorio atual

git config --global #muda configurações do computador

git config --local user.name "nome" #altera nome usuario
git config --local user.email "email" #altera email do usuario
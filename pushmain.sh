#!/bin/bash

TextoCommit="$1"

# Associa o repositório remoto ao repositório local.          
    git remote add origin git@github.com:paulosspacheco/gitignore.git

# Renomeie o branch  atual para main
# O comando branch -M não precisa ser feito a todo momento, porque o git sempre envia para
# o ultimo ramo selecionando.
    git branch -M main  

# Este comando pode ser executado várias vezes antes de um commit.  
    git add .

# Use o <msg> fornecido como a mensagem de confirmação. 
    git commit -a -m "$TextoCommit"

# Envia as alterações locais para o repositório remoto.
    git push -u origin main                  

# imprime o status atual do repositório
 git status  




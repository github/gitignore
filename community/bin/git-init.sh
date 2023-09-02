#! /bin/bash

GIT_INIT_PATH=$(echo -e "${GIT_INIT_PATH:=~/.local/share/gitignore}")

help() {

    echo -e "\ngit-init: A git init script to initialize a new git repository with a .gitignore file"
    echo -e "          copied from the github/gitignore repository\n"

    echo -e "usage: git-init [project-type]\n"

    echo -e "    project-type\tThe prefix used for a .gitignore file."
    echo -e "\n"

    echo -e "Running the git-init command without a project-type will generate a defauly empty .gitignore file"

    echo -e "The GIT_INIT_PATH sets the path that the github/gitignore repository is stored in."
    echo -e "The default path is ~/.local/share/gitignore\n"

    echo -e "Setting the environment variable GIT_INIT_EXTRAS_FOLDER will create a .extras folder to store files"
    echo -e "that may be useful to keep locally but the git repository should ignore.\n"

    exit
}

gitignore () {  

    if [ -f .gitignore ]; then

        return
    fi

    if [ $# -eq 0 ]; then  

        echo -e "# Default .gitignore" > .gitignore
        return

    else
        GITIGNORE_FILE=$(find $GIT_INIT_PATH -iname "$1.gitignore")
    fi

    if [ -z $GITIGNORE_FILE ]; then

        echo -e "Unknown gitignore file type: $1"
        echo -e "see available types in \n\t${GIT_INIT_PATH}"
        exit 1
    fi

    if [ ! -f $GITIGNORE_FILE ]; then

        echo -e "Missing $GITIGNORE_FILE"
        return
    fi

    cp $GITIGNORE_FILE .gitignore
    echo -e "Create .gitignore file for $1\n"
    head -n 3 .gitignore
    echo
}

gitextras () {

    if [ -n "$GIT_INIT_EXTRAS_FOLDER" ]; then 

        mkdir -p $(pwd)/.extras    
        echo -e "\n\n# Extra files kept locally but ignored in the repository\n.extras/\n" >> .gitignore
    fi    
}

if [ "$1" == "-h" ]|| [[ "$1" == "--help" ]]; then
    help
fi

gitignore $1
gitextras

if [ ! -d .git ]; then

    git init
fi

# Git-Init script

The git-init script is designed to initialize a new git repository using the 
files from the github/gitignore file list.

This script can be run inside an initialized git repository if no .gitignore file
already exist. The script will not overwrite any existing .gitignore or reinitialize
a git repository.

## Installation

Clone the github/gitignore repository to your ~/.local/share folder

```
    git clone https://github.com/github/gitignore
```

Create a link in your ~/.local/bin folder (or in any other bin folder in your PATH variable)
called git-init to the git-init.sh file.

```
    ln -s ~/.local/share/gitignore/community/bin/git-init.sh ~/.local/bin/git-init
```

You can clone the repository to another folder and then set the
GIT_INIT_PATH environment variable.

```
    GIT_INIT_PATH=/path/to/gitignore
```

## Usage

Run the git-init script with the name of a prefix in the github/gitignore file list.

```
    git-init [project-type]

    project-type    The prefix used for a .gitignore file.
```

Examples:

```
    # Initialize a C project using the C.gitignore file
    git-init c

    # Initialize a Node project using the Node.gitignore file
    git-init node
```

Running the git-init command without a project-type will generate a default empty .gitignore file

## Environment configuration

The GIT_INIT_PATH sets the path that the github/gitignore repository is stored in. 
The default path is ~/.local/share/gitignore

```
    export GIT_INIT_PATH=/path/to/gitignore

```

Setting the environment variable GIT_INIT_EXTRAS_FOLDER will create a .extras folder to store files
that may be useful to keep locally but the git repository should ignore.

```
    export GIT_INIT_EXTRAS_FOLDER=true
```

## Requirements

The script requires the following tools:

`git`, `bash` and `find`
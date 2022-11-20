#!/usr/bin/env python3

' update git ignore list. '

import os


def get_root_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.split(script_dir)[0]


def list_files(path):
    fs = [f for f in os.listdir(path) if f.endswith('.gitignore')]
    fs.sort()
    return fs


def gen_js(ignores):
    s = ['\'' + ig[:-10] + '\'' for ig in ignores]
    return '[' + ', '.join(s) + ']'


def main():
    root_dir = get_root_dir()
    print(f'detect root dir: {root_dir}')
    language_ignores = list_files(root_dir)
    global_ignores = list_files(os.path.join(root_dir, 'Global'))

    js = f'''
// auto-generated ignore list:
window.language_ignores = {gen_js(language_ignores)};
window.global_ignores = {gen_js(global_ignores)};
'''
    print(js)
    with open(os.path.join(root_dir, 'script', 'gitignore.js'), 'w') as f:
        f.write(js)


if __name__ == '__main__':
    main()

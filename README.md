# A Collection of Useful .gitignore Templates

That's what we're trying to build. Please contribute
by [forking][fk] and sending a [pull request][pr].

Also **please** only modify **one file** per commit. This'll
make merging easier for everyone.

Global gitignores (OS-specific, editor-specific) should go into the
`Global/` directory.

For more information on gitignore: [gitignore(5)][g5]

[fk]: http://help.github.com/forking/
[pr]: http://help.github.com/pull-requests/
[g5]: http://man.cx/gitignore

## Pull Requests

Since this repo includes a large and diverse
number of programming languages, frameworks, editors,
and ecosystems, it's **very helpful** if you can provide 
a link to information supporting your pull request. 
Up-to-date, canonical documentation that mentions the files 
to be ignored is best.

This ensures we can efficiently go through pull requests
and keep quality high.

## Global Ignores

git has a global configuration that applies rules to all of
your projects. For example:

    git config --global core.excludesfile ~/.global_ignore

... will apply the rules in ~/.global_ignore for all of your repos.

This is useful if you use an editor (like Emacs) that drops backup files,
or if you work in an environment that generates binary or intermediate
files that are always ignored.

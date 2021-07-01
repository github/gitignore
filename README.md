# A collection of `.gitignore` templates

This is GitHub’s collection of [`.gitignore`][man] file templates.
We use this list to populate the `.gitignore` template choosers available
in the GitHub.com interface when creating new repositories and files.

For more information about how `.gitignore` files work, and how to use them,
the following resources are a great place to start:

- The [Ignoring Files chapter][chapter] of the [Pro Git][progit] book.
- The [Ignoring Files article][help] on the GitHub Help site.
- The [gitignore(5)][man] manual page.

[man]: http://git-scm.com/docs/gitignore
[help]: https://help.github.com/articles/ignoring-files
[chapter]: https://git-scm.com/book/en/Git-Basics-Recording-Changes-to-the-Repository#_ignoring
[progit]: http://git-scm.com/book

## Folder structure

We support a collection of templates, organized in this way:

- The root folder contains templates in common use, to help people get started
  with popular programming languages and technologies. These define a meaningful
  set of rules to help get started, and ensure you are not committing
  unimportant files into your repository.
- [`Global`](./Global) contains templates for various editors, tools and
  operating systems that can be used in different situations. It is recommended
  that you either [add these to your global template](https://help.github.com/articles/ignoring-files/#create-a-global-gitignore)
  or merge these rules into your project-specific templates if you want to use
  them permanently.
- [`community`](./community) contains specialized templates for other popular
  languages, tools and project, which don't currently belong in the mainstream
  templates. These should be added to your project-specific templates when you
  decide to adopt the framework or tool.

## What makes a good template?

A template should contain a set of rules to help Git repositories work with a
specific programming language, framework, tool or environment.

If it's not possible to curate a small set of useful rules for this situation,
then the template is not a good fit for this collection.

If a template is mostly a list of files installed by a particular version of
some software (e.g. a PHP framework), it could live under the `community`
directory. See [versioned templates](#versioned-templates) for more details.

If you have a small set of rules, or want to support a technology that is not
widely in use, and still believe this will be helpful to others, please read the
section about [specialized templates](#specialized-templates) for more details.

Include details when opening pull request if the template is important and visible. We
may not accept it immediately, but we can promote it to the root at a later date
based on interest.

Please also understand that we can’t list every tool that ever existed.
Our aim is to curate a collection of the _most common and helpful_ templates,
not to make sure we cover every project possible. If we choose not to
include your language, tool, or project, it’s not because it’s not awesome.

## Contributing guidelines

We’d love for you to help us improve this project. To help us keep this collection
high quality, we request that contributions adhere to the following guidelines.

- **Provide a link to the application or project’s homepage**. Unless it’s
  extremely popular, there’s a chance the maintainers don’t know about or use
  the language, framework, editor, app, or project your change applies to.

- **Provide links to documentation** supporting the change you’re making.
  Current, canonical documentation mentioning the files being ignored is best.
  If documentation isn’t available to support your change, do the best you can
  to explain what the files being ignored are for.

- **Explain why you’re making a change**. Even if it seems self-evident, please
  take a sentence or two to tell us why your change or addition should happen.
  It’s especially helpful to articulate why this change applies to _everyone_
  who works with the applicable technology, rather than just you or your team.

- **Please consider the scope of your change**. If your change is specific to a
  certain language or framework, then make sure the change is made to the
  template for that language or framework, rather than to the template for an
  editor, tool, or operating system.

- **Please only modify _one template_ per pull request**. This helps keep pull
  requests and feedback focused on a specific project or technology.

In general, the more you can do to help us understand the change you’re making,
the more likely we’ll be to accept your contribution quickly.

## Versioned templates

Some templates can change greatly between versions, and if you wish to contribute
to this repository we need to follow this specific flow:

- the template at the root should be the current supported version
- the template at the root should not have a version in the filename (i.e.
  "evergreen")
- previous versions of templates should live under `community/`
- previous versions of the template should embed the version in the filename,
  for readability

This helps ensure users get the latest version (because they'll use whatever is
at the root) but helps maintainers support older versions still in the wild.

## Specialized templates

If you have a template that you would like to contribute, but it isn't quite
mainstream, please consider adding this to the `community` directory under a
folder that best suits where it belongs.

The rules in your specialized template should be specific to the framework or
tool, and any additional templates should be mentioned in a comment in the
header of the template.

For example, this template might live at `community/DotNet/InforCRM.gitignore`:

```
# gitignore template for InforCRM (formerly SalesLogix)
# website: https://www.infor.com/product-summary/cx/infor-crm/
#
# Recommended: VisualStudio.gitignore

# Ignore model files that are auto-generated
ModelIndex.xml
ExportedFiles.xml

# Ignore deployment files
[Mm]odel/[Dd]eployment

# Force include portal SupportFiles
!Model/Portal/*/SupportFiles/[Bb]in/
!Model/Portal/PortalTemplates/*/SupportFiles/[Bb]in
```

## Contributing workflow

Here’s how we suggest you go about proposing a change to this project:

1. [Fork this project][fork] to your account.
2. [Create a branch][branch] for the change you intend to make.
3. Make your changes to your fork.
4. [Send a pull request][pr] from your fork’s branch to our `master` branch.

Using the web-based interface to make changes is fine too, and will help you
by automatically forking the project and prompting to send a pull request too.

[fork]: https://help.github.com/articles/fork-a-repo/
[branch]: https://help.github.com/articles/creating-and-deleting-branches-within-your-repository
[pr]: https://help.github.com/articles/using-pull-requests/

## License

[CC0-1.0](./LICENSE).

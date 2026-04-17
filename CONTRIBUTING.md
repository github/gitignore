# Contributing guidelines

We’d love you to help us improve this project. To help us keep this collection
high quality, we request that contributions adhere to the following guidelines.
Any contributions that don't meet these guidelines will be closed.

- **Provide a link to the application or project’s homepage**. Unless it’s
  extremely popular, there’s a chance the maintainers don’t know about or use
  the language, framework, editor, app, or project your change applies to.

- **Provide a reason for making this change**. Even if it seems self-evident,
  please take a sentence or two to tell us why your change or addition should
  happen. It’s especially helpful to articulate why this change applies to
  *everyone* who works with the applicable technology, rather than just you or
  your team.

- **Provide links to documentation** supporting the change you’re making.
  Current, canonical documentation mentioning the files being ignored is best.
  If documentation isn’t available to support your change, do the best you can
  to explain what the files being ignored are for.

- **Keep scope as limited as possible**. Changes should be as small as possible
  and apply to the most specific gitignore template available for the target
  application. For example: OS-specific ignore rules like `.DS_Store` are not
  accepted anywhere but their specific gitignore, `Global/macOS.gitignore` in
  this case.

- **Only modify *one template* per pull request**. This helps keep pull
  requests and feedback focused on a specific project or technology.

- **Add new rules to the most appropriate existing section**. Please ensure
  your contribution does not create duplicate sections or add rules in
  unrelated sections.

- **No duplicate rules**. It's easy to do, but it creates confusion and
  introduces the risk of one or the other being missed in an update.

In general, the more you can do to help us understand the change you’re making,
the more likely we’ll be to accept your contribution quickly.

If a template is mostly a list of files installed by a particular version of
some software (e.g. a PHP framework) then it's brittle and probably no more
helpful than a simple `ls`. If it's not possible to curate a small set of
useful rules, then the template is not a good fit for this collection.

Please also understand that we can’t list every tool that ever existed.
Our aim is to curate a collection of the *most common and helpful* templates,
not to make sure we cover every project possible. If we choose not to
include your language, tool, or project, it’s not because it’s not awesome.

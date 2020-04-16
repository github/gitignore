# Gitignore Metadata

This document outlines the additional metadata that can be associated with a gitignore template, and how tools can consume this metadata.

## Metadata Location

To add additional metadata to a gitignore template, add a new file to the same directory, with the matching name but ending in `yml`.

For example:
 - for `C.gitignore` the associated metadata will be stored in `C.yml`
 - for `Global/JetBrains.gitignore` the metadata file will be `Global/JetBrains.gitignore`

## Supported Fields

The structure of these files is still being settled upon, but for the moment these are some proposed entries.

#### `aliases`

Some templates can be used to represent a number of different situations, and rather than duplicating files on disk and needing to keep these in sync, we can store a list of these entries as metadata.

For example, JetBrains has a unified gitignore template that can be applied to all of their IDEs. Previously these were stored as comments in the header:

```
# Covers JetBrains IDEs: IntelliJ, RubyMine, PhpStorm, AppCode, PyCharm, CLion, Android Studio and WebStorm
```

These values can be represented as metadata, so that tools consuming this repository can use these entries as matches if the user is searching for a specific product:

```yaml
aliases:
  - IntelliJ
  - RubyMine
  - PhpStorm
  - AppCode
  - PyCharm
  - CLion
  - Android Studio
  - WebStorm
  - Rider
```

#### `editors`

There are a number of editors out there that support working with different languages. Rather than baking every editor's rules in every language that is supported, a list of additional templates that might be of interest

```yaml
editors:
  - Global/JetBrains.gitignore
  - Global/VisualStudioCode.gitignore
```

#### `reference`

Some ecosystems have up-to-date documentation about things that are necessary to exclude from version control. To associate this with a template, this could be stored as a key-value pair in metadata:

```yaml
reference: https://intellij-support.jetbrains.com/hc/en-us/articles/206544839
```

### `reviewers`

This element is inspired by the [`DefinitelyTyped`](https://github.com/DefinitelyTyped/DefinitelyTyped) project, allowing community members to opt-in to reviewing templates when a pull request is opened. This helps to share the review load and credit people who have been helpful with reviews.

```yaml
reviewers:
  - @shiftkey
```

A friendly name can be provided alongside the GitHub account name.

```yaml
reviewers:
  - Brendan Forster (@shiftkey)
```

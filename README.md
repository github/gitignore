# Gitignore Guide

A comprehensive, organized, and categorized collection of `.gitignore` templates for your projects.

## Why this repository?

`.gitignore` files tell Git which files and directories to ignore in a project. A good `.gitignore` prevents secrets, generated code, and local environment files from being pushed to your repository.

This project organizes templates by category to make it easy for developers to find what they need.

## Folder Structure

The repository is structured logically to help you find templates quickly:

```text
Gitignore-Guide/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── templates/
    ├── build-tools/
    ├── cloud/
    ├── community/
    ├── databases/
    ├── design-and-cad/
    ├── devops/
    ├── editors-and-ides/
    ├── frameworks/
    ├── game-development/
    ├── hardware/
    ├── languages/
    ├── misc/
    ├── mobile/
    ├── operating-systems/
    ├── testing/
    ├── text-processing/
    ├── tools-and-misc/
    └── version-control/
```

- **`templates/<category>`**: Mainstream templates sorted by their primary domain (e.g., `languages/Python.gitignore`, `frameworks/Rails.gitignore`, `operating-systems/macOS.gitignore`).
- **`templates/community/`**: Specialized templates for niche tools or older versions that don't belong in the mainstream templates.

## How to Use

1. Find the template(s) you need in the `templates/` directory.
2. Copy the contents into your project's `.gitignore` file.
3. If you use multiple technologies (e.g., Python + VSCode + macOS), you should combine the contents of `templates/languages/Python.gitignore`, `templates/editors-and-ides/VisualStudioCode.gitignore`, and `templates/operating-systems/macOS.gitignore`.

## Contributing

We welcome contributions! If you'd like to add a missing template, fix a bug, or improve documentation, please read our [Contributing Guidelines](CONTRIBUTING.md).

Here is the general workflow:

1. Fork the repository.
2. Create a branch for your feature.
3. Place your template in the appropriate `templates/<category>/` directory. (If it's niche or highly specific, place it in `templates/community/`).
4. Submit a pull request.

## License

This project is licensed under [CC0-1.0](./LICENSE).

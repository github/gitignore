import os
import shutil

categories = {
    "languages": [
        "Actionscript", "Ada", "Agda", "Ballerina", "C++", "C", "Clojure", "CommonLisp", "Coq", "D", "Dart", "Delphi", "Elisp",
        "Elixir", "Elm", "Erlang", "Fortran", "Go", "Haskell", "Haxe", "Idris", "Java", "Julia", "Kotlin", "Lean", "Lua", "Luau",
        "Mercury", "Nim", "OCaml", "Objective-C", "Perl", "Python", "R", "Racket", "Raku", "ReScript", "Ruby", "Rust", "Scala",
        "Scheme", "Smalltalk", "Solidity-Remix", "Swift", "VBA", "Zig", "Dotnet", "Deno", "Gleam", "HIP", "MoonBit", "Opa", "Processing",
        "PureScript", "Sdcc"
    ],
    "frameworks": [
        "Angular", "AppEngine", "CakePHP", "CodeIgniter", "Concrete5", "CraftCMS", "Drupal", "ExpressionEngine", "ExtJs", "FuelPHP",
        "Grails", "Joomla", "Laravel", "Magento", "Nestjs", "Nextjs", "Node", "OpenCart", "Phalcon", "PlayFramework", "Prestashop",
        "Qt", "Rails", "Symfony", "SymphonyCMS", "TurboGears2", "Typo3", "WordPress", "Yii", "ZendFramework", "CFWheels", "Lithium",
        "RhodesRhomobile", "SeamGen", "Zephir", "bun"
    ],
    "mobile": [
        "Android", "AppceleratorTitanium", "Flutter", "GWT"
    ],
    "game-development": [
        "AdventureGameStudio", "FlaxEngine", "Godot", "Unity", "UnrealEngine", "DM"
    ],
    "build-tools": [
        "CMake", "Composer", "Gradle", "Maven", "Nix", "Packer", "Waf", "Yeoman"
    ],
    "cloud": [
        "Firebase", "GitHubPages", "Salesforce", "ForceDotCom"
    ],
    "devops": [
        "Autotools", "ChefCookbook", "Terraform", "JENKINS_HOME", "ROS", "ecu.test", "Gcov"
    ],
    "operating-systems": [
        "Linux", "macOS", "Windows", "ArchLinuxPackages"
    ],
    "editors-and-ides": [
        "Eclipse", "Emacs", "JetBrains", "NotepadPP", "SublimeText", "Vim", "VisualStudioCode", "Xcode", "VisualStudio",
        "Eagle", "IAR", "KiCad", "ModelSim", "STM32CubeIDE", "XilinxISE", "Zed", "Kate", "Lazarus", "NetBeans"
    ],
    "databases": [
        "OracleForms", "Redis"
    ],
    "testing": [
        "Katalon", "TestComplete"
    ],
    "design-and-cad": [
        "SolidWorks", "SketchUp", "Modelica"
    ],
    "text-processing": [
        "TeX", "GitBook", "Jekyll", "Nanoc", "Textpattern", "Scrivener"
    ],
    "hardware": [
        "CUDA", "LabVIEW", "Lasal", "TwinCAT3", "Stella"
    ],
    "misc": [
        "AL", "Archives", "Backup", "Diff", "GPG", "Images", "Tags"
    ]
}

def move_files():
    base_path = "."
    
    # Create category directories
    for cat in categories.keys():
        os.makedirs(os.path.join(base_path, "templates", cat), exist_ok=True)
        
    os.makedirs(os.path.join(base_path, "templates", "uncategorized"), exist_ok=True)
    
    def get_category(name):
        base_name = name.replace(".gitignore", "")
        for cat, items in categories.items():
            if base_name in items:
                return cat
        return "uncategorized"
        
    def process_dir(d):
        if not os.path.isdir(d):
            return
        for f in os.listdir(d):
            if f.endswith(".gitignore"):
                src = os.path.join(d, f)
                cat = get_category(f)
                dst = os.path.join(base_path, "templates", cat, f)
                shutil.move(src, dst)

    process_dir(base_path)
    process_dir(os.path.join(base_path, "Global"))
    
    # community has subdirectories, let's just move everything to templates/community for now
    # or better, just leave community where it is, or merge it. The prompt says: "if appropriate... Do NOT blindly use this exact structure. Design the taxonomy based on what actually exists in the repository."
    # Let's move community to templates/community
    if os.path.exists(os.path.join(base_path, "community")):
        os.makedirs(os.path.join(base_path, "templates", "community"), exist_ok=True)
        for item in os.listdir(os.path.join(base_path, "community")):
            src = os.path.join(base_path, "community", item)
            dst = os.path.join(base_path, "templates", "community", item)
            shutil.move(src, dst)
        shutil.rmtree(os.path.join(base_path, "community"))
        
    if os.path.exists(os.path.join(base_path, "Global")):
        shutil.rmtree(os.path.join(base_path, "Global"))

if __name__ == "__main__":
    move_files()

import os
import shutil

base_path = "."
uncategorized_path = os.path.join(base_path, "templates", "uncategorized")

categories = {
    "version-control": ["Bazaar", "CVS", "Mercurial", "SVN", "TortoiseGit"],
    "devops": ["Ansible", "Vagrant", "Lefthook", "mise"],
    "frameworks": ["EPiServer", "Kohana", "LemonStand", "Plone", "SugarCRM", "Qooxdoo"],
    "editors-and-ides": ["Anjuta", "BricxCC", "Cloud9", "CodeKit", "Cursor", "DartEditor", "Dreamweaver", "EiffelStudio", "Ensime", "Espresso", "FlexBuilder", "JDeveloper", "KDevelop4", "MonoDevelop", "Momentics", "Redcar", "SlickEdit", "TextMate"],
    "languages": ["Fancy", "Xojo"],
    "tools-and-misc": []
}

def move_files():
    if not os.path.exists(uncategorized_path):
        return
        
    for cat in categories.keys():
        os.makedirs(os.path.join(base_path, "templates", cat), exist_ok=True)
        
    for f in os.listdir(uncategorized_path):
        if not f.endswith(".gitignore"):
            continue
        base_name = f.replace(".gitignore", "")
        
        target_cat = "tools-and-misc"
        for cat, items in categories.items():
            if base_name in items:
                target_cat = cat
                break
                
        os.makedirs(os.path.join(base_path, "templates", target_cat), exist_ok=True)
        src = os.path.join(uncategorized_path, f)
        dst = os.path.join(base_path, "templates", target_cat, f)
        shutil.move(src, dst)
        
    if not os.listdir(uncategorized_path):
        os.rmdir(uncategorized_path)

if __name__ == "__main__":
    move_files()

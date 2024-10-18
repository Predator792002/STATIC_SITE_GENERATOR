from text_node import TextNode
import os
import shutil

import os
import shutil

def copy_directory(src, dst):
    # Ensure destination directory exists and is empty
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    # List all items in source directory
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            # If it's a directory, recursively copy it
            copy_directory(s, d)
        else:
            # If it's a file, copy it
            shutil.copy2(s, d)
        print(f"Copied: {s} to {d}")


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()
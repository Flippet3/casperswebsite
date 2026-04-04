import os
import shutil
from casperswebsite.general_tools import get_root_folder

if __name__ == "__main__":
    root_folder = get_root_folder()
    compiled_dir = os.path.join(root_folder, "compiled")
    print(compiled_dir)

    # Delete all files (and folders) in the compiled directory
    if os.path.exists(compiled_dir):
        for filename in os.listdir(compiled_dir):
            file_path = os.path.join(compiled_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(compiled_dir)

    # Generate dummy index.html
    index_html_path = os.path.join(compiled_dir, "index.html")
    dummy_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dummy HTML Page</title>
</head>
<body>
  <h1>Welcome to the Dummy HTML Page</h1>
  <p>This is a placeholder page for testing purposes.</p>
</body>
</html>
"""
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(dummy_html)
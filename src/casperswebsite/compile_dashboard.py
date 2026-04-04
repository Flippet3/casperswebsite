import os
import shutil
from casperswebsite.dashboard.pages.authors_page import AuthorsPage
from casperswebsite.dashboard.pages.home import HomePage
from casperswebsite.dashboard.pages.howitsmade import HowItsMadePage
from casperswebsite.dashboard.pages.resume import ResumePage
from casperswebsite.dashboard.pages.storyguide import StoryGuidePage
from casperswebsite.dashbuilder.renderer import render_pages
from casperswebsite.general_tools import get_root_folder

if __name__ == "__main__":
    root_folder = get_root_folder()
    compiled_dir = os.path.join(root_folder, "compiled")

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

    rendered_pages = render_pages([HomePage(), AuthorsPage(), HowItsMadePage(), StoryGuidePage(), ResumePage()])
    for endpoint, html in rendered_pages.items():
        out_dir = os.path.join(compiled_dir, endpoint)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

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

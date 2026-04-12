import os
import shutil
from casperswebsite.dashboard.pages.authors_page import AuthorsPage
from casperswebsite.dashboard.pages.energy_simulation import EnergySimulationPage
from casperswebsite.dashboard.pages.home import HomePage
from casperswebsite.dashboard.pages.jasmin import Jasmin
from casperswebsite.dashboard.pages.howitsmade import HowItsMadePage
from casperswebsite.dashboard.pages.resume import ResumePage
from casperswebsite.dashboard.pages.storyguide import StoryGuidePage
from casperswebsite.dashbuilder.renderer import render_pages
from casperswebsite.general_tools import get_root_folder

if __name__ == "__main__":
    root_folder = get_root_folder()
    compiled_dir = os.path.join(root_folder, "compiled")
    tmp_backup = os.path.join(root_folder, "_compile_tmpbak")
    static_src = os.path.join(root_folder, "src", "casperswebsite", "static")
    static_dst = os.path.join(compiled_dir, "static")

    try:
        # Move existing compiled_dir contents to tmp_backup
        if os.path.exists(compiled_dir):
            if os.path.exists(tmp_backup):
                shutil.rmtree(tmp_backup)
            os.makedirs(tmp_backup)
            for item in os.listdir(compiled_dir):
                src = os.path.join(compiled_dir, item)
                dst = os.path.join(tmp_backup, item)
                shutil.move(src, dst)
        else:
            os.makedirs(compiled_dir)

        rendered_pages = render_pages(
            [
                HomePage(),
                AuthorsPage(),
                HowItsMadePage(),
                StoryGuidePage(),
                ResumePage(),
                EnergySimulationPage(),
                Jasmin(),
            ]
        )
        for endpoint, html in rendered_pages.items():
            out_dir = os.path.join(compiled_dir, endpoint)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.html")
            if endpoint == "Home":
                with open(os.path.join(compiled_dir, "index.html"), "w", encoding="utf-8") as f:  # fmt: skip
                    f.write(html)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)

        # Symlink compiled/static to src/casperswebsite/static
        # Remove any existing file or symlink first
        if os.path.islink(static_dst) or os.path.exists(static_dst):
            if os.path.islink(static_dst) or os.path.isfile(static_dst):
                os.unlink(static_dst)
        os.symlink(static_src, static_dst)

        # Success, remove backup
        if os.path.exists(tmp_backup):
            shutil.rmtree(tmp_backup)
    except Exception as e:
        # Rollback on failure
        print(f"Dashboard compilation failed: {e}")
        if os.path.exists(compiled_dir):
            shutil.rmtree(compiled_dir)
        if os.path.exists(tmp_backup):
            shutil.move(tmp_backup, compiled_dir)
        raise

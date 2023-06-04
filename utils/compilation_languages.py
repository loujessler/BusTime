import os
import subprocess


def compile_translations(LOCALES_DIR):
    for root, dirs, files in os.walk(LOCALES_DIR):
        for file in files:
            if file.endswith('.po'):
                po_path = os.path.join(root, file)
                mo_path = os.path.join(root, file.rsplit('.', 1)[0] + '.mo')
                subprocess.run(['msgfmt', po_path, '-o', mo_path], check=True)

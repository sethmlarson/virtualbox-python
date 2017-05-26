import os
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(base_dir, 'docs', 'build')
if os.path.isdir(build_dir):
    shutil.rmtree(build_dir)

os.chdir(os.path.join(base_dir, 'docs'))
os.system('make html')

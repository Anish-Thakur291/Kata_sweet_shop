import os
import sys
import runpy

script_dir = os.path.dirname(__file__)
manage_path = os.path.abspath(os.path.join(script_dir, "..", "manage.py"))
sys.argv = [manage_path] + sys.argv[1:]
runpy.run_path(manage_path, run_name="__main__")

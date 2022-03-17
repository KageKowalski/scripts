# Utility functions for interacting with the OS


# Imports
import os
import time


# Deletes all files contained in "directory" (string)
# If "days" (int) is passed a value, only files that were last modified "days" (int) days ago or more are deleted
# Only deletes directories in addition to files if ignore_directories (bool) is set to False
def clean_dir(directory, days=0, ignore_directories=True):
    now = time.time()
    for item in os.scandir(directory):
        if os.stat(item).st_mtime <= now - days * 86400:
            if ignore_directories and item.is_file():
                os.remove(item.path)
            elif not ignore_directories and (item.is_file() or item.is_dir()):
                os.remove(item.path)

# Deletes everything in the log directory that is DAYS_OLD days old or older, including directories


# Imports
import env_var
from os_util import clean_dir


# Constants
LOG_DIR = env_var.LOG_PATH
DAYS_OLD = 29
IGNORE_DIRECTORIES = False


# Clean log directory
clean_dir(LOG_DIR, DAYS_OLD, IGNORE_DIRECTORIES)

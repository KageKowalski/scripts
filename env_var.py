# Contains environment variables to be imported by scripts
#
# Template for environment variable exports on a Linux machine:
# "
# export SCRIPTS_PATH=/home/USER/scripts/
# export DIR_PATH=${SCRIPTS_PATH}/dir/
# export CRED_PATH=${DIR_PATH}/.cred/
# export LOG_PATH=${DIR_PATH}/.log/
# "


# Imports
from os import environ


# Pull environment variables from OS
try:
    SCRIPTS_PATH = environ["SCRIPTS_PATH"]
except KeyError:
    print("ERROR: Define SCRIPTS_PATH in system environment variables.")
try:
    DIR_PATH = environ["DIR_PATH"]
except KeyError:
    print("ERROR: Define DIR_PATH in system environment variables.")
try:
    CRED_PATH = environ["CRED_PATH"]
except KeyError:
    print("ERROR: Define CRED_PATH in system environment variables.")
try:
    LOG_PATH = environ["LOG_PATH"]
except KeyError:
    print("ERROR: Define LOG_PATH in system environment variables.")

# 1. Delete NP environment
# 2. Re-create NP environment
# 3. Copy relevant PRD environment info to NP environment
#
# Must be run as root


# Constants
NP_USERNAME="scriptrunner_np"
PRD_USERNAME="scriptrunner"


# 1. Delete NP environment
echo "Step #1"
deluser --remove-home $NP_USERNAME


# 2. Re-create NP environment
echo "Step #2"
adduser --disabled-password --gecos "" $NP_USERNAME


# 3. Copy relevant PRD environment info to NP environment
echo "Step #3"
rsync -a --chown={$NP_USERNAME}:{$NP_USERNAME} /home/{$PRD_USERNAME}/scripts/ /home/{$NP_USERNAME}/scripts/

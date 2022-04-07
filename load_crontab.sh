# Load crontab

CRONTAB_FILE=${CRON_PATH}crontab.txt
echo "Installing crontab file ${CRONTAB_FILE}"
crontab "$CRONTAB_FILE"
echo "NEW CRONTAB CONTENTS"
echo
crontab -l

#!/bin/bash

#rm -f log/*.log

python experiment.py

#Notify phone about the script completion
telegram_sendmessage "Your experiment has finished."

#Send log file to telegram
LOG_FILE=log/$(ls log -1 | tail -n 1)
telegram_sendfile $LOG_FILE
#!/bin/bash

export GIT_SSH_COMMAND='ssh -i ~/.ssh/id_rsa_pwless -o IdentitiesOnly=yes'
today=$(date --date "-4 hours" +"%Y-%m-%d")
output=$(git add . 2>&1 && git commit -m "Daily Commit: $today" 2>&1 && git push 2>&1) \
    || (echo "$output" && mailx -s "Git auto commit failure." -r "henry@localhost" "henry@localhost" <<< "$output")
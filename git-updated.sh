#!/bin/bash
git config --global user.name 'github-actions[bot]'
git config --global user.email 'github-actions[bot]@users.noreply.github.com'

# Check for staged changes
git diff --cached --quiet # returns 1 when there are staged changes  
exit_code=$?


if [[ $exit_code -ne 0 ]]; then 
    git commit -m 'Update results data'
    git push 
    curl -X POST -H "Accept: application/vnd.github.v3+json" -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/pokerpanther/pokerpanther.github.io/dispatches -d '{"event_type":"changes_detected"}'
else
    echo "No changes to commit."
fi

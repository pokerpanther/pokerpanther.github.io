#!/bin/bash

# Check for staged changes
git diff --cached --quiet
exit_code=$?


if [[ $exit_code -ne 0 ]]; then 
    git commit -m 'Update results data'
    git push
else
    echo "No changes to commit."
fi

# git diff --cached --quiet returns 1 when there are staged changes  
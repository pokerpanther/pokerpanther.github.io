if [[ ! git diff --cached --quiet ]]; then 
    git commit -m 'Update results data'
    git push
else
    echo "No changes to commit."
fi

# git diff --cached --quiet returns 1 when there are staged changes  
## create a new branch
``git switch -c docs/git``

## get the latest content from main
``git pull origin main``

## check the changes of a particular file 
``git diff``

``git switch --chaced`` if in staging

then modify content in such a way

## push to git if it's done
``git add -p``
``git commit -am "docs: meaningful comments"``
``git push -u origin docs/git``

> merge the new content on github

## once it has merged then remove the unused branch
``git push -u origin --delete docs/git``
``git branch -D docs/git`` 

> delete branch from remote and local 
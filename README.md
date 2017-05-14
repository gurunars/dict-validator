# python-build-scripts

Install into the repo:

    cd ${GIT_REPO_NAME}
    git remote add build-scripts git@github.com:gurunars/python-build-scripts.git
    git subtree add —-prefix=build-scripts/ build-scripts master
    ln -s build-scripts/Makefile Makefile
    cp build-scripts/travis.yml.in .travis.yml

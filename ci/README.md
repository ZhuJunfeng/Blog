# Continuous Integration System
A simple continuous integration system forked from [500lines](https://github.com/aosabook/500lines/tree/master/ci).
This system will detect new commit periodically and run tests against it.

## Usage
```bash
$ mkdir path/to/test_repo
$ cd path/to/test_repo
$ git init
$ git clone path/to/test_repo path/to/test_repo_observer
$ git clone path/to/test_repo path/to/test_repo_runner

$ python dispatcher.py
$ python observer.py path/to/test_repo_observer
$ python test_runner.py path/to/test_repo_runner
```

## The components
### Observer
Observer monitors a repository and notifies the dispatcher the newest commit id when it detects a new commit. The observer uses `git log` to get the newest commit id.

### Dispatcher


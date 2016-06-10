# Continuous Integration System
A simple continuous integration system in [500lines](https://github.com/aosabook/500lines/tree/master/ci).
This system will detect new commit periodically and run tests against it.

## The components
### Observer
The observer monitors a repository and notifies the dispatcher the newest commit id by using `git log`.

### Dispatcher
The dispatcher sets up a simple server and manages a list of test runners. Once it receives `dispatch` command from the observer, it dispatch the test job to an idle test runner. The dispatcher will remove a test runner from the list when it goes down and redistribute the test job to another test runner if the job hasn't finished.

### Test Runner
The test runner also sets up a simple server. When a test runner is invoked, it will send `register` command to the dispatcher. When it receives a commit id, it will run tests against it and return the results.

## Conclusion
1. The system shows how a simple CI system works.
2. The system consists of multiple processes and each process communicates with each other by setting up a simple server. It also shows how to use `heartbeat` to check whether the other side is up and still running and how to handle error when the other side is down.

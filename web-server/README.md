# Web-server
A simple web server in [500lines](https://github.com/aosabook/500lines/tree/master/web-server).

## Conclusion

1. Construct multiple classes which have methods like `test()` and `act()` to get rid of a long tangle of `if` statements
```python
class case_no_file(base_case):
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

...
Cases = [case_no_file(),
        case_cgi(),
        case_existing_file()]

...
for case in self.Cases:
    if case.test(self):
        case.act(self)
        break
```
2. Extensiblity. People can add a new functionality by adding a case handler class.



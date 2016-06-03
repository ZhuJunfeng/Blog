# Web-server
A simple web server forked from [500lines](https://github.com/aosabook/500lines/tree/master/web-server).

## Usage

```bash
$ python web_server.py
```
1. Serve static pages
`http://localhost:8080/index.html`
2. List directories
`http://localhost:8080/resource`
3. Support CGI protocol
`http://localhost:8080/cgi.py`

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



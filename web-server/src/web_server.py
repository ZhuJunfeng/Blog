import BaseHTTPServer
import os

class ServerException(Exception):
    pass


class base_case(object):
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)

        except IOError as msg:
            msg = "'{0}' cannnot be read: {1}".format(handler.path, msg)
            handler.handle_error(msg)

    
class case_no_file(base_case):
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class case_existing_file(base_case):
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class case_dir_with_index(base_case):
    def index_path(self, full_path):
        return full_path + 'index.html'

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler.full_path))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler.full_path))


class case_dir_without_index(base_case):
    Listing_Page = '''\
<html>
<body>
<ul>
{0}
</ul>
</body>
</html>
'''
    def handle_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(entry)
                       for entry in entries if not entry.startswith('.')]
            content = self.Listing_Page.format('\n'.join(bullets))
            handler.send_content(content)
        except OSError as msg:
           msg = "'{0}' cannot be listed: {1}".format(handler.path, msg)
           handler.handle_error(msg)


    def index_path(self, full_path):
        return full_path + 'index.html'

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler.full_path))

    def act(self, handler):
        self.handle_dir(handler, handler.full_path)


class case_cgi(base_case):
    def handle_cgi(self, handler, full_path):
        cmd = 'python ' + full_path
        child_stdin, child_stdout = os.popen2(cmd)
        child_stdin.close()
        content = child_stdout.read()
        child_stdout.close()
        handler.send_content(content)


    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')

    def act(self, handler):
        self.handle_cgi(handler, handler.full_path)


class case_unknown_object(base_case):
    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    Cases = [case_no_file(),
             case_cgi(),
             case_existing_file(),
             case_dir_with_index(),
             case_dir_without_index(),
             case_unknown_object()]

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path

            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)


    Error_Page = '''\
<html>
<body>
<h1>Error accessing {path}</h1>
<p>{msg}</p>
</body>
</html>
'''
    def handle_error(self, msg):
        content = self.Error_Page.format(path = self.path, msg = msg)
        self.send_content(content, 404)


    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()

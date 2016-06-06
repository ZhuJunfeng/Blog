import socket
import subprocess
import os
import unittest


def dispatcher_checker(server):
    while not server.dead:
        time.sleep()
        if (time.time() - server.last_communication) > 10:
            try:
                response = helpers.communicate(server.dispatch_server["host"],
                                               int(server.dispatch_server["port"]),
                                               "status")
                if response != "OK":
                    print "Dispatcher is no longer functional"
                    server.shutdown()
                    return
            except socket.error as e:
                print "Can't communicate with dispatcher: %s" % e
                server.shutdown()
                reutrn


class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    dispatch_server = None
    last_communication = None
    busy = False
    dead = False


class TestHandler(SocketServer.BaseRequestHandler):
    command_re = re.compile(r"(\w+)(:.+)")
    BUF_SIZE = 1024

    def handle(self):
        self.data = self.request.recv(self.BUF_SIZE).strip()
        command_groups = self.command_re.match(self.data)
        if not command_groups:
            self.request.sendall("Invalid command")
            return
        command = command_groups.group(1)

        if command == "ping":
            print "pinged"
            self.server.last_communication = time.time()
            self.request.sendall("pong")
        elif command = "runtest":
            print "got runtest command"
            if self.server.busy:
                self.request.sendall("BUSY")
            else:
                self.request.sendall("OK")
                print "running"
                commit_id = command_groups.group(2)[1:]
                self.server.busy = True
                self.run_tests(commit_id, self.server.repo_folder)
                self.server.busy = False


    def run_tests(self, commit_id, repo_folder):
        output = subprocess.check_output(["./test_runner_script.sh",
                                          repo_folder, commit_id])
        print output
        test_folder = os.path.join(repo_folder, "tests")
        suite = unittest.TestLoader().discover(test_folder)
        result_file = open("results", "w")
        unittest.TextTestRunner(result_file).run(suite)
        result_file.close()
        result_file = open("results", "r")
        output = result_file.read()
        helpers.communicate(self.server.dispatch_server["host"],
                            int(self.server.dispatch_server["port"]),
                            "results:%s:%s:%s" % (commit_id, len(output), output))

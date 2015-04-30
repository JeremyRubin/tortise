from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from os import urandom
import socks
import socket
def create_connection(address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

import urllib2
import urllib
msgs = set([])
peers = set([])
class HelloHandler(RequestHandler):
    def get(self):
        for msg in msgs:
            self.write(msg)
            self.write("<br><br>")
        self.write("""
        <form method="POST">
        <input type="textarea" name="msg">
        <input type="submit">
        </form>
        <br>
        Want to run a node? Grab a copy of the code <a href="https://github.com/JeremyRubin/tortise"> here </a>
        """)
    def post(self):
        msg = self.get_argument("msg")
        if not msg in msgs:
            msgs.add(msg)
            data = urllib.urlencode({"msg":msg})
            for peer in peers:
                req = urllib2.Request(url=peer,data=data)
                urllib2.urlopen(req).read()
        self.get()


class PeerHandler(RequestHandler):
    def post(self):
        peers.add(self.get_argument("peer"))
        self.get()
    def get(self):
        self.write("""
        <form method="POST">
        <input type="textarea" name="peer">
        <input type="submit">
        </form>
        <br>
        Want to run a node? Grab a copy of the code <a href="https://github.com/JeremyRubin/tortise"> here </a>
        """)

        
def make_app():
    return Application([
        url(r"/", HelloHandler),
        url(r"/peer", PeerHandler),
    ])

def main():
    app = make_app()
    app.listen(8083)
    IOLoop.current().start()

if __name__ == "__main__":
    main()

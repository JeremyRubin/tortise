import tornado.escape
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from os import urandom
import socks
import socket
# You can ignore this section for now; it's a patch to use our tor connection
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
import time

# Server State: A set of messages, and a set of peers to send information to
msgs = set([])
peers = set([])

class HomeHandler(RequestHandler):
    """When the user visits the main page, show them the messages and a form to submit a new msg"""
    def get(self):
        # for every message...
        for (t, msg) in sorted(list(msgs)):
            # Prevent unescaped html from leaking
            # (try removing this, and submitting a message with html!)
            m = tornado.escape.xhtml_escape(msg) 
            t = tornado.escape.xhtml_escape(t) 

            
            # Write out the message, and some space
            self.write(t)
            self.write("<br>")
            self.write(m) 
            self.write("<br><br>") 
        # Write out the form to submit a new message
        self.write("""
            <h3> Add New Message </h3>
            <form method="POST">
            <input type="textarea" name="msg">
            <input type="submit">
            </form>
            <br>
            Want to run a node? Grab a copy of the code <a
            href="https://github.com/JeremyRubin/tortise"> here </a> """)

        # Show the visitor a form to add a peer.
        self.write("""
            <h3> Add a Peer  </h3>
            <h4> (enter in http://&lt;hostname&gt;/ format) </h4>
            <form method="POST" action="/peer">
            <input type="textarea" name="peer">
            <input type="submit">
            </form>""")
        self.write("<br><h3> Connected To </h3>")
        for p in peers:
            self.write(tornado.escape.xhtml_escape(p))
    def post(self):
        # Get the submitted message (fail otherwise)
        msg = self.get_argument("msg")

        # Check to see if we already have seen
        # this message, ignore if we have.
        # (why might that be the case?)

        # Add the message
        msgs.add((str(time.time()),msg))

        # Show the visitor the homepage again
        self.get()


class PeerHandler(RequestHandler):
    """ Page where visitors can subscribe their instance to yours """
    def post(self):
        # get the peer's url
        peer = self.get_argument("peer")
        # Add the peer
        peers.add(peer)


        # Show the visitor the main page
        self.redirect("/")
    def get(self):
        self.write(tornado.escape.json_encode(list(msgs)))
        
def make_app():
    """ Set up the URL Routing """
    return Application([
        url(r"/", HomeHandler),     # Make the homepage handled by HomeHandler
        url(r"/peer", PeerHandler), # Do the same for peering
    ])
def check_peers():
    # Get messages from all of our peers
    print "RUN"
    for peer in peers:
        req = peer+"peer"
        result =urllib2.urlopen(req).read()
        l = tornado.escape.json_decode(result)
        final = map(tuple, l)
        msgs.update(final)

def main():
    app = make_app()
    # comminicate via port 8083
    app.listen(8084)
    tornado.ioloop.PeriodicCallback(check_peers, 10000).start()
    # Start the App
    IOLoop.current().start()


# When we run `python run.py`
if __name__ == "__main__":
    main()

Install Tor Browser: https://www.torproject.org/


Add the following lines to your torrc file.
You'll need to customize the directory paths.


My torrc is located at: /Applications/TorBrowser.app/TorBrowser/Data/Tor/torrc

Factoid: the -rc suffix doesn't really stand for anything useful, but you can think of it as resource configuration.

```
HiddenServiceDir /Users/jeremyrubin/tortise/priv 
HiddenServicePort 80 127.0.0.1:8083
```

Need help? https://www.torproject.org/docs/tor-hidden-service.html.en has more detailed instructions





(Re)Start TorBrowser.






in src/, run `python run.py`

You may need some dependencies:
`pip install PySocks`
`pip install tornado`







check priv/hostname to see your onion address (keep key in priv private)


Paste the address into the Tor Browser to connect.


visit /peer on your website to put your friends domains (ie, http://<hostname>/ in and send/recieve messages

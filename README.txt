Install Tor Browser


Add the following lines to your torrc. You'll need to customize the paths.


(Mine is located at: /Applications/TorBrowser.app/TorBrowser/Data/Tor/torrc)

```
HiddenServiceDir /Users/jeremyrubin/tortise/priv 
HiddenServicePort 80 127.0.0.1:8083
```


(Re)Start TorBrowser.

`pip install PySocks`
`pip install tornado`

in src/, run `python run.py`

check priv/hostnmae to see your onion address (keep key in priv private)

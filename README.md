# Background Information

The idea behind this supplemental material was to create a hidden service on Tor that initial users of the dark web would go to and trust by mistake. 

This hidden service hopes to highlight a few errors new users make. First, new Tor users do not realize that downloading content while on Tor has the potential to expose their actual IP address and identity, so the site sets up an appealing download that when opened can unmask the user. Next, the site offers assistance to access the SilkRoad, perhaps the most famous hidden service. For a new user, it can be intimidating and hard to use, and in order to access any illegal material on the SilkRoad, the new user must register. The site thus provides a "list" of already registered username and password combinations for download, that when downloaded actually runs a python script to get the user's ip.

In essence, the hidden service I created, called Silky, causes problems for users by preying on the usability and mystery of the SilkRoad while highlighting that most users do not fully understand how to keep their anonymity of origin secure.     

## Downloadable Content from Silky

The python script is disguised as a fake username and password list.

The script uses libraries `urlopen` and `getpass` to retrieve the ip address and username of the user running the script.

Next, the script utilizes `twilio` to send a message to a phone number containing the ip and username. Twilio requires prior set up to use the pre-registered number and also needs a corresponding confirmed phone number for the receiving text message. For the receiving number, I set up a free burner phone number on top of my iPhone in order to mask my actual phone number and forward these twilio messages through it.

Upon double clicking the script, the user gets no indication that the program has run, and my phone gets a notification with the users public IP and username.

The app is available under `/silky/list.txt.app.zip`

#### Creation of the app from python script

Using `pyinstaller` in the directory as the python script, run:

`pyinstaller --onefile --windowed list.txt.py`

which will yield an executable `list.txt.app` file in 'path/to/directory/dist'

#### Next Steps + Future Modifications

###### Windows exe and File Name

From a mac machine, which is the one I used to make all supplemental materials, it seems difficult to construct a Windows Executable. I did attempt to run `wine` coupled with `pyinstaller` but was never successful. Furthermore, if a windows exe is indeed created, it is possible to further obfuscate the file name by using the unicode right-to-left override character `U+202E` such that the file `NotMaliciousSoftwaretxt.exe` would display as `NotMaliciousSoftwareexe.txt`, leading the user to open the app thinking that it was a text file.

###### Other

- Send User data to a server instead of a burner phone
- Get MAC Address of user instead of just username and ip

#### Known Issues

Currently, downloading the .app or .zip file containing the bundled python script in the app results in an error though sending the bundled script via Facebook Messenger works or directly downloading the app from my github repo also runs.

Also, app is designed to work on OS X El Capitan, and has not yet worked on OS X Yosemite.

## Configuring Hidden Service

I found [this tutorial](http://www.makeuseof.com/tag/create-hidden-service-tor-site-set-anonymous-website-server/) helpful for some troubleshooting.

To configure a hidden service, I first modified the supplied `torrc` file to contain
```
HiddenServiceDir /Users/Isaiah/torHidden
HiddenServicePort 80 127.0.0.1:80
```
Upon running `tor` in the terminal and opening TorBrowser, I received a `hostname` and `private_key` in my `torHidden` directory.

I used the `hostname` khbyuvngsdelpyo3.onion to configure the server.

## Server

I primarily used [this tutorial](https://medium.com/@JohnFoderaro/how-to-set-up-apache-in-os-x-10-11-el-capitan-637b30fe67b1) along with a few stackoverflow posts to patch my system.

I am using Apache2 as my underlying server. In short, I modified my .conf file in order to set up the initial site:

```
<Directory "/Users/Isaiah/Sites/">
  AllowOverride All
  Options Indexes MultiViews FollowSymLinks
  Require all granted
</Directory>
```
I next set up a VirtualHost with the hidden service given to me by Tor

```
<VirtualHost *:80>
  ServerName khbyuvngsdelpyo3.onion
  ServerAlias www.silky.localhost
  DocumentRoot "/Users/Isaiah/Sites/silky"
  ErrorLog "/private/var/log/apache2/silky-error_log"   
  CustomLog "/private/var/log/apache2/silky-access_log" common
  <Directory "/Users/Isaiah/Sites/silky">
    RewriteEngine On
    Options -Indexes
    #WWW to HTTP
    RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
    RewriteRule ^ http://%1%{REQUEST_URI} [R=301,L]
    #Remove Index.html
    RewriteCond %{THE_REQUEST} ^GET\ .*/index\.html
    RewriteRule ^(.*)index\.html$ /$1 [R=301,L]
  </Directory>
</VirtualHost>
```
Finally I ran `sudo apachectl restart` and was able to view the site both on my TorBrowser at 
`khbyuvngsdelpyo3.onion` and `http://localhost/~Isaiah/silky/`

## Disclaimer

Though my server is not vulnerable to [this](https://thehackernews.com/2016/02/apache-tor-service-unmask.html) Apache misconfiguration, the fact that my computer is unable to keep my server constantly running leaks information to any observant adversary. [This](https://nvd.nist.gov/vuln/detail/CVE-2017-9798) vulnerability is also a threat to my personal data. Because of this, I have decided to default turn it off, and provide screenshots. If anyone would like to see it working, please contact me directly.

## Tests

Tests can be seen in screenshots folder.

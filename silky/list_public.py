from urllib2 import urlopen
import getpass
import twilio
import twilio.rest

my_ip = urlopen('http://ip.42.pl/raw').read()

usr = getpass.getuser()

from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "***************"
# Your Auth Token from twilio.com/console
auth_token  = "***************"

client = Client(account_sid, auth_token)

msg_string = "IP: %s, USR: %s" % (my_ip, usr)

message = client.messages.create(
    to="+1**********", 
    from_="+1**********", #twilio number
    body=msg_string)
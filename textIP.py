from twilio.rest import Client
import os

def textIPtoRahat(msg):
    client = Client("AC09e045976b218be8ae4b29a37465b9be", os.environ.get("TWILIO"))
    client.messages.create(to="+14077660001", from_="+14195498636", body=str(msg))
    return True # if failed then wouldthrow error

from twilio.rest import Client

def textIPtoRahat(msg):
    client = Client("AC09e045976b218be8ae4b29a37465b9be", "40f4727cda22b5205aa006cc2e2847b4")
    client.messages.create(to="+14077660001", from_="+14195498636", body=str(msg))

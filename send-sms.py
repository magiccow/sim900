import nexmo
import configparser

config = configparser.ConfigParser()
config.read('sms.ini')

client = nexmo.Client(key=config['DEFAULT']['key'], secret=config['DEFAULT']['secret'])

result = client.send_message({
    'to': '447700900601',    # number of the SIM900 module
    'from': 'Vonage APIs',
    'text': 'Bright Star, would I were constant as thou art'
})

print(f"Send SMS returned {result}")

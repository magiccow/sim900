# sim900-gsm

Sample code for PC application receiving SMS via serial-attached SIM 900 GSM Module.  (read-sms.py)
Repo also contains send-sms.py which uses cloud service Nexmo/Vonage to send test text messages 
module. This is derived from the Nexmo sample code; don't forget to pip3 install nexmo, and also put
your own Nexmo keys into sms.ini. 

read-sms.py uses Python3 and serial library, so should work on RaspPi also.

See  also YouTube video:

https://youtu.be/KVI7BhXEJ3o

https://youtube.com/c/martyndavies


The SIM 800 and M590E GSM modules also have very similar AT command sets. The SMS receive code in this
repo should be good for these modules also.

See also: Tutorial on the SIM800 module: https://youtu.be/8rqfPc8aRGc


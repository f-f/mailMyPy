import imaplib, parselib

# dict for credentials
login = {}

f = open('login.conf', 'r')
login['username'] = f.readline().rstrip('\n')
login['password'] = f.readline().rstrip('\n')
f.close()

print login

try:
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(login['username'],login['password'])
	pass
except mail.error:
	raise mail.error, "Connection Error!"
else: # if connection not succeeds imap raises an error, else it prints 
	print "Connected."

mail.select('INBOX')

result, ids = mail.search(None, "ALL") #result should be 'OK'
idList = ids[0].split() # ids[0] is a space separated string

for i in range(0,len(idList)):
	#fetching all emails by id
	body = mail.fetch(idList[-i-1], "(UID BODY[TEXT])") #starting from last email
	rawEmail = body[0][1]

	#here goes the template parsing, the matching and the mail sending
	#functions for that are in parselib
	#parsed messages should be deleted?

mail.close()
mail.logout()
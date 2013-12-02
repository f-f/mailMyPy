import imaplib, mmplib, email

# dict for credentials
login = {}

f = open('login.conf', 'r')
login['username'] = f.readline().rstrip('\n')
login['password'] = f.readline().rstrip('\n')
login['label'] = f.readline().rstrip('\n')
f.close()

#let's connect
mail = mmplib.imapConnect(login)

#get the mails that are in the label (ordered by id)
idList = mmplib.getLabelMails(login, mail)

#fetch'em
for i in range(0,len(idList)):
	
	result, data = mail.uid('fetch', idList[-i-1], '(RFC822)') #"(UID BODY[TEXT])")
	rawEmail = data[0][1]

	#convert the ugly raw in something better
	emailMessage = email.message_from_bytes(rawEmail)

	#some useful stuff to print?
	print(emailMessage['To'])
	print(email.utils.parseaddr(emailMessage['From']))
	print(emailMessage.items()) # print all headers

	#this gets the body, cleaned and ready for lxml
	print(mmplib.getMultipartMailText(emailMessage))

	#here goes the template parsing, the matching and the mail sending
	#and the archiviation too

mmplib.imapDisconnect(mail)
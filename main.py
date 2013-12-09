import imaplib, mmplib, email, string

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
	#print(emailMessage['To'])
	#print(emailMessage.items()) # print all headers

	#parsing the FROM field
	rawFROM = email.utils.parseaddr(emailMessage['From'])
	FROM = rawFROM[(string.find(rawFROM,"<")):string.find(rawFROM,">") + 1)]

	#this gets the body, cleaned
	print(mmplib.getMultipartMailText(emailMessage))

	#pathsList is a dictionary from an external file
	myDataList = matchTemplates(pathsList, FROM, rawEmail)

	mailData['to'] = myDataList['email']
	mailData['subject'] = "some subject"
	mailData['text'] = "so text"

	sendEmail(login,mailData)

mmplib.imapDisconnect(mail)
import imaplib, mmplib, email, string
from templates import pathsList

# dict for credentials
login = {}

f = open('login.conf', 'r')
login['username'] = f.readline().rstrip('\n')
login['password'] = f.readline().rstrip('\n')
login['label'] = f.readline().rstrip('\n')
f.close()

print(login)

#let's connect
mail = mmplib.imapConnect(login)

#get the mails that are in the label (ordered by id)
idList = mmplib.getLabelMails(login, mail)

#fetch'em
for i in range(0, 1):#len(idList)):
	
	result, data = mail.uid('fetch', idList[-i-1], '(RFC822)') #"(UID BODY[TEXT])")
	rawEmail = data[0][1]

	#convert the ugly raw in something better
	#emailMessage = email.message_from_bytes(rawEmail)
	emailMessage = email.message_from_string(rawEmail.decode('utf-8'))

	#some useful stuff to print?
	#print(emailMessage['To'])
	#print(emailMessage.items()) # print all headers

	#parsing the FROM field
	rawFROM = email.utils.parseaddr(emailMessage['From'])
	print("FROM:",rawFROM[1])
	FROM = rawFROM[1]

	#this gets the body, cleaned and decoded
	decodedMail = mmplib.getMultipartMailText(emailMessage).decode('ascii')

	#pathsList is a dictionary from an external file
	myDataList = mmplib.matchTemplates(pathsList, FROM, decodedMail)

	mailData = {}
	#mailData['to'] = myDataList['email'] <---- in real case
	mailData['to'] = "vincenzo.ampolo@gmail.com"
	mailData['subject'] = "mailMyPy, first try."
	mailData['text'] = "Ciao! Questa mail dovrebbe andare a '%s', proprietario dell'indirizzo '%s', e cliente di %s.\n\n" %(myDataList['name'],myDataList['email'],FROM)
	
	#mark it as (un)seen
	mail.store(idList[-i-1], '-FLAGS', '(\Seen)')

	print(mailData)
	#mmplib.sendEmail(login,mailData)

mmplib.imapDisconnect(mail)

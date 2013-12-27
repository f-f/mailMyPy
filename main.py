import imaplib, mmplib, email, string
from templates import pathsList

# dict for credentials
login = {}

f = open('login.conf', 'r')
login['username'] = f.readline().rstrip('\n')
login['password'] = f.readline().rstrip('\n')
login['label'] = f.readline().rstrip('\n')
login['dbString'] = f.readline().rstrip('\n')
f.close()

#let's connect
mail = mmplib.imapConnect(login)

#get the mails that are in the label (ordered by id)
idList = mmplib.getLabelMails(login, mail)

#we create the postgre engine and the session
engine = mmplib.createEngine(login['dbString'])
session = mmplib.createDbSession(engine)

mailCounter = 0

#fetch'em
for i in range(0, len(idList)):
	
	result, data = mail.uid('fetch', idList[-i-1], '(RFC822)') #"(UID BODY[TEXT])")
	rawEmail = data[0][1]

	#database part
	actualHash = mmplib.mailHash(rawEmail)
	if mmplib.md5RowCheck(session, actualHash): #if the hash is in the db jump
		print("The hash '%s' is already in the database!" %(actualHash))
		continue

	#convert the ugly raw in something better
	emailMessage = email.message_from_string(rawEmail.decode('utf-8'))

	#parsing the FROM field
	rawFROM = email.utils.parseaddr(emailMessage['From'])
	FROM = rawFROM[1]

	#this gets the body, cleaned and decoded
	decodedMail = mmplib.getMultipartMailText(emailMessage).decode('utf-8')

	#pathsList is a dictionary from an external file: templates.py
	myDataList = mmplib.matchTemplates(pathsList, FROM, decodedMail)

	#let's cut the shit off
	if myDataList['email']=="":
		continue #this is for messages that don't match the template

	#database insert
	mmplib.insertMailRow(session, myDataList, FROM, actualHash)

	mailData = {}
	mailData['to'] = myDataList['email']
	mailData['subject'] = "Your subject"
	
	#we import the template for the mail that is going to be sent
	with open ("template.html", "r") as tempFile:
		tempString=tempFile.read() #.replace('\n', '')

	mailData['text'] = tempString.encode('ascii','ignore').decode("utf-8")

	#mark it as seen
	mail.store(idList[-i-1], '+FLAGS', '(\Seen)')

	print("Name: %s, Mail: %s, From: %s" %(myDataList['name'],myDataList['email'],FROM))

	#print(mailData)
	if mmplib.sendEmail(login,mailData):
		mailCounter+=1

print(len(idList))
print("Sent %s mails." %(mailCounter))

mmplib.imapDisconnect(mail)

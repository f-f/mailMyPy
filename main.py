import imaplib, mmplib

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
	
	rawEmail = mail.fetch(idList[i], "(UID BODY[TEXT])")

	#here goes the template parsing, the matching and the mail sending
	#and the archiviation too

mmplib.imapDisconnect(mail)
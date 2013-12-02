from lxml import etree
import imaplib, smtplib, email


###### IMAP

def imapConnect(login):
	try:
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		mail.login(login['username'],login['password'])
		pass
	except mail.error:
		raise Exception("Connection Error!")
		return False
	else: # if connection not succeeds imap raises an error, else it prints 
		print("Connected.")
	
	return mail

def imapDisconnect(mail):
	mail.close()
	mail.logout()

def getLabelMails(login, mail): #mail is the imap handler

	mail.select(mailbox = login['label'], readonly = False) #after login, it selects the label specified in config

	#parse the folder and get the emails by uid
	result, ids = mail.uid('search', None, "ALL") #search and return uids, result should be 'OK'
	idList = ids[0].split() # ids[0] is a space separated string

	return idList

###### Email

# If you want to get text content (body) and the email contains 
# multiple payloads (plaintext/ html), you must parse each message separately
# This function is taken from a stackoverflow post:
def getMultipartMailText(emailMessage):
    maintype = emailMessage.get_content_maintype()
    if maintype == 'multipart':
        for part in emailMessage.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return emailMessage.get_payload()


###### SMTP

def sendEmail(login, mailData): #mailData is a dictionary
	FROM = login['username']
	TO = [mailData['to']] #must be a list
	SUBJECT = mailData['subject']
	TEXT = mailData['text']

	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
		server.ehlo()
		server.starttls()
		server.login(login['username'], login['password'])
		server.sendmail(FROM, TO, message)
		server.close()
		print('Successfully sent the mail')
		return True
	except:
		print("Failed to send mail")
		return False


###### Xpath

def parseTemp(templatePath):
	#doc = etree.parse(f)
	return #it returns an xpath, actually unused, the xpaths list is stored in xpaths.py

#given an xpath, it returns the email from the Blob
def pickEmail(xpath, mailBlob):
	return
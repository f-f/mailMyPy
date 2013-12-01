from lxml import etree
import imaplib

def getLabelMails(login):
	try:
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		mail.login(login['username'],login['password'])
		pass
	except mail.error:
		raise(mail.error, "Connection Error!")
	else: # if connection not succeeds imap raises an error, else it prints 
		print("Connected.")

	mail.select(login['label']) #after login, it selects the label specified in config

	#parse the folder and get the emails by id
	result, ids = mail.search(None, "ALL") #result should be 'OK'
	idList = ids[0].split() # ids[0] is a space separated string

	mail.close()
	mail.logout()

	return idList

def parseTemp(templatePath):
	#doc = etree.parse(f)
	return #it returns an xpath, actually unused, the xpaths list is stored in xpaths.py

#given an xpath, it returns the email from the Blob
def pickEmail(xpath, mailBlob):
	return 

def sendMail(address):
	return #sends mail to address (using a template for that?) and returns success code
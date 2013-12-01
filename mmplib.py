from lxml import etree
import imaplib, smtplib

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
		return TRUE
	except:
		print("Failed to send mail")
		return FALSE


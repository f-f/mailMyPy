import imaplib, smtplib, email, re, sqlalchemy, hashlib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import etree


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

def parseUid(data):
	match = re.compile('\d+ \(UID (?P<uid>\d+)\)').match(data)
	return match.group('uid')


###### Email

# If you want to get text content (body) and the email contains 
# multiple payloads (plaintext/ html), you must parse each message separately
# This function is taken from a stackoverflow post:
def getMultipartMailText(emailMessage):
	maintype = emailMessage.get_content_maintype()
	if maintype == 'multipart':
		payload = []
		for part in emailMessage.get_payload():
			if part.get_content_maintype() == 'text':
				payload.append(part.get_payload(decode=True).decode('utf-8'))
		return ''.join(payload).encode('ascii','ignore')
	elif maintype == 'text':
		return emailMessage.get_payload().encode('ascii','ignore')


###### SMTP

def sendEmail(login, mailData): #mailData is a dictionary
	FROM = login['username']
	TO = mailData['to']
	SUBJECT = mailData['subject']
	TEXT = mailData['text']

	# Create message container - the correct MIME type is multipart/alternative.
	message = MIMEMultipart('alternative')
	message['Subject'] = SUBJECT
	message['From'] = FROM
	message['To'] = TO
	#message['Bcc'] = "example@gmail.com"

	part1 = MIMEText(TEXT, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	message.attach(part1)
	
	try:
		#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
		server.ehlo()
		#server.starttls()
		server.login(login['username'], login['password'])
		server.sendmail(FROM, TO, message.as_string()) #in case of multiple destination che TO field is a list with the emails
		server.close()
		print('Successfully sent the mail')
		return True
	except:
		print("Failed to send mail")
		raise
		return False

###### Xpath

#given a path, it returns the data from the mail
def pickData(mypath, mailBody):
	myTree = etree.HTML(mailBody)
	r = myTree.xpath(mypath)
	if len(r)==0:
		r.append("")
	return str(r[0])

#pathsList example:
# pL = [ {email: em@example.com, paths: [{name: "email", path: "/example/..."}, ...]}, ...]

#this function picks the list with the templates and checks if matches, then picks the data
def matchTemplates(pathsList,FROM, mailBody):
	data = {}
	for item in pathsList:
		if FROM == item['email']: # <== template matching is here
			for paths in item['paths']: #item['paths'] is a list for data, that contains a dict
				data[paths['name']] = pickData(paths['path'],mailBody)
	return data


###### Database - Sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
	__tablename__ = 'emails'

	md5 = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	email = sqlalchemy.Column(sqlalchemy.String)
	origin = sqlalchemy.Column(sqlalchemy.String)
	timestamp = sqlalchemy.Column(sqlalchemy.Float)

	def __repr__(self):
	   return "<Mail(name='%s', email='%s', origin='%s', timestamp='%s')>" % (
	                        self.name, self.email, self.origin, self.timestamp)

def createEngine(connectionString):
	engine = sqlalchemy.create_engine(connectionString, encoding='latin1', echo=True)
	Base.metadata.create_all(engine)
	return engine

def createDbSession(engine):
	from sqlalchemy.orm import sessionmaker
	Session = sessionmaker(bind=engine)
	session = Session()
	print("Database table '%s' ready." %(User.__table__))
	return session

def mailHash(rawEmail):
	newHash = hashlib.md5(rawEmail.decode('utf-8').encode("ascii","ignore")).hexdigest()
	return newHash

def insertMailRow(session, myDataList, FROM, newHash):
	#insertion
	newMailRecord = User(md5=newHash, name=myDataList['name'], email=myDataList['email'], origin=FROM, timestamp=time.time())
	session.add(newMailRecord)
	session.commit()

def md5RowCheck(session, actualHash):
	hashExist = session.query(User).filter_by(md5=actualHash).first()
	if hashExist: return True
	return False
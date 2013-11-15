from lxml import etree

def parseTemp(templatePath):
	#doc = etree.parse(f)
	return #it returns an xpath, actually unused, the xpaths list is stored in xpaths.py

#given an xpath, it returns the email from the Blob
def pickEmail(xpath, mailBlob):
	return 

def sendMail(address):
	return #sends mail to address (using a template for that?) and returns success code
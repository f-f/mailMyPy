from lxml import etree

f = open('temp1.eml', 'r')
doc = ""
for line in f:
	line = line.replace('=\n','\n')
	line = line.rstrip('\n')
	line = line.replace('3D"','"')
	line = line.replace('</br>','')

	doc+=line

#print doc

parser = etree.XMLParser(remove_blank_text=True, recover=True)
myTree = etree.XML(doc, parser)

#r = myTree.xpath('/div')
#print r

print(etree.tostring(myTree, pretty_print=True))

f.close()
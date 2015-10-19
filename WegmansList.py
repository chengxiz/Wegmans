#The List 'WSL_List' will contain following data :
#	1. NAME, e.g., '22: Wegmans West Seneca'
#	2. ADDRESS, e.g., '370 Orchard Park Rd.'
#	3. CITY, e.g., 'West Seneca'
#	4. STATE, e.g.,'NY'
#	5. ZIP CODE, e.g., '14224'
#	6. REGION, e.g., 'Buffalo'
#	7. LOCATION, e.g. '42.8348383, -78.7842068, 21'
#	8. LINK to 'make this my store'

def WegmansListGet(HtmlCodes):
	import re
	prefix='http://www.wegmans.com/webapp/wcs/stores/servlet/'

	WSL_List=[]
	Basic=re.findall('<a\shref.*?<script',HtmlCodes,re.S)[0]
	#Four Situtaion should be taken into account for Regex Expression:
	#	1.Three words:
	#		Wegmans Alberta Drive	
	#	2.Two words:
	#		Wegmans Auburn
	#	3.Two words with '-':
	#		Wegmans Chili-Paul
	#	4.Three words with '.': 
	#		Wegmans Mt. Read ##This is the TROUBLESOME one so I have to use (A|B) expression
	#		B has concluded the other 3 types and A is speical for the fourth one
	NAME_Dict=re.findall('(Wegmans\s\w*.\s\w*|Wegmans\s\w*\s?-?\w*)',Basic,re.S)[0]
	NAME=re.findall('(\d+:\sWegmans\s\w*.\s\w*|\d+:\sWegmans\s\w*\s?-?\w*)',Basic,re.S)[0]
	WSL_List.append(NAME)
	for m in re.findall('<td>.*</td>',Basic):
		#print(m.group())
		m=re.sub('<td>','',m)
		m=re.sub('</td>','',m)
		#print(m)
		WSL_List.append(m)
	LOCATION=re.findall('createMarkerFromLoc\(.*?\s"',HtmlCodes)[0]
	LOCATION=re.sub('createMarkerFromLoc\(','',LOCATION)
	LOCATION=re.sub('"','',LOCATION)
	WSL_List.append(LOCATION)
	LINK=re.findall('a\shref=Weg.*?<img',HtmlCodes)[0]
	LINK=re.sub('a\shref=','',LINK)
	LINK=re.sub('><img','',LINK)
	LINK=prefix+LINK
	WSL_List.append(LINK)
	return NAME_Dict, WSL_List
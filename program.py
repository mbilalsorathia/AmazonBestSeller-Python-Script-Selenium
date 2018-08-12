from selenium import webdriver
#from selenium.webdriver.common.keys import keys
from bs4 import BeautifulSoup, NavigableString
import time
import pandas as pd
import math
import codecs
from googletrans import Translator
import datetime
import os
now = datetime.datetime.now()

domainList = {
'IN' : 'in','CN' : 'cn',
'JP' : 'co.jp','SG' : 'com.sg',
'FR' : 'fr','DE' : 'de',
'IT' : 'it','NL' : 'nl',
'ES' : 'es','UK' : 'co.uk',
'CA' : 'ca','MX' : 'com.mx',
'US' : 'com','AU' : 'com.au',
'BR' : 'br' }

df = pd.read_csv('BSRINPUT.csv')

try:
	os.stat("BSROUTPUT.csv")
	output=codecs.open('BSROUTPUT.csv','a','utf-8')	
except:
	output=codecs.open('BSROUTPUT.csv','a','utf-8')
	output.write('PRODUCT,Country,TITLE,BSR,PRICE,Category,Date\n')

driver = webdriver.Chrome()
lines=df['URL ']
cat=df['Category ']
translator = Translator()
cg=0
a7=str(now.strftime("%Y-%m-%d %H:%M"))
for i in lines:			
	cate=cat[cg]
	cate=cate.upper()
	cg=cg+1
	url1=i
	url12=url1[:url1.find('/gp')]
	country=''
	for i in domainList:
		if url12.find(domainList[i])!=-1:
			country= i
	count=0
	for i in range(0,2):
		if i==0:
			url=url1
			count=0
		elif i==1:
			url=url1+'?ie=UTF8&pg=2'
			count=50
		print url
		time.sleep(3)
		driver.get(url)
		src=driver.page_source
		soup=BeautifulSoup(src,'html.parser')
		v=''
		try:
			#print 'aaaaa'a-column a-span12 a-text-center
			v=soup.findAll('span',{'class':'aok-inline-block zg-item'})
#			print '1'
			for j in v:
				a1=j.find('a')
				a1=a1['href']
				a1=a1[a1.find('/dp')+4:a1.find('/ref')-1]
				output.write(a1+',')
#				print '2'
				a2=country.upper()
#				print '3'
				output.write(a2+',')
				
				a3=j.find('img')
				a3=a3['alt']
				a3=translator.translate(a3).text
				a3=a3.replace(',','')
#				print '4'
				output.write(a3+',')
				
				a4=count+1
#				print '5'
				output.write(str(a4)+',')
				
				count=count+1
				a5=''
				try:
					a5=j.find('span',{'class':'p13n-sc-price'})
					a5=a5.get_text()
					a5=a5.replace(',','.')
					output.write(a5+',')
				except:
					a5=''
					output.write(',')
				#print 'yes'
				a6=cate
				output.write(a6+',')
				output.write(a7+'\n')
#				print '6'
#				output.write(a1+','+a2+','+a3+','+a4+'\n')
		except:
	#		v=''
			print 'err'
			#output.write('\n')
				
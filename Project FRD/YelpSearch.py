from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request as urllib2
import re
import requests
import json
import csv

def process():
	try:
		data=[]
		api_key = 'LQLTUs3aqkwAjHD05EkOcH9QkUFo4F0W3x9OizxIm86Ie-U9uKB0XM3T0b1EeD5g-6cP_WiN_Sh9GhKY-XZq01RfQjmyEHVx5hUKUgdLyx48NkmfzIrM_cb1H5OyXXYx'
		headers = {'Authorization': 'Bearer %s' % api_key}
		url = 'https://api.yelp.com/v3/businesses/search'
		params = {'term':"Restaurant",'location':"11249"}
		req = requests.get(url, params=params, headers=headers)
		parsed = json.loads(req.text)
		#print(parsed)
		businesses = parsed["businesses"]
		for business in businesses:
			print(business)
			#print("ID:",business["id"])
			#print("Name:", business["name"])
			#print("Rating:", business["rating"])
			#print("Address:", " ".join(business["location"]["display_address"]))
			ad=" ".join(business["location"]["display_address"])
			#print("Phone:", business["phone"])
			print("zipcode:", business["location"]["zip_code"])
			#print("state:", business["location"]["state"])
			#print("Review_count:", business["review_count"])
			#print("\n")
		
			name=business["name"]
			print("Name of the Restaurant",name)
			url=business["url"]
			print(url)
			soup2 = BeautifulSoup(urllib2.urlopen(url).read())
			print(soup2)
			reviews = soup2.findAll('div', {"itemprop":"review"})
			print(reviews)
			for m in reviews:
				print("***************")
				author=m.findAll('meta', {"itemprop":"author"})
				author1=str(author[0]).split("\"")
				print(author1[1])
				rating=m.findAll('meta', {"itemprop":"ratingValue"})
				rating1=str(rating[0]).split("\"")
				print(rating1[1])
				datep=m.findAll('meta', {"itemprop":"datePublished"})
				datep1=str(datep[0]).split("\"")
				print(datep1[1])
				clean = re.compile('<.*?>')
				m1=re.sub(clean, '', str(m))
				review=m1.strip()
				print("Review",review)
				friends = m.find('span', {'class':'i-wrap ig-wrap-common_sprite i-18x18_friends_c-common_sprite-wrap'})
				print(friends)
				data.append([business["id"],business["name"],ad,business["phone"],business["location"]["zip_code"],business["location"]["state"],business["review_count"],business["rating"],author1[1],datep1[1],review,"REAL"])
				print("***************")
			urls=url.split("?")
			bizname=urls[0].split("/")
			
			print(bizname[4])
		
			soup3 = BeautifulSoup(urllib2.urlopen(urljoin('http://www.yelp.com/not_recommended_reviews/',bizname[4])).read())
			#print(soup3)
			filteredreviews = soup3.findAll('div', attrs={'class':re.compile(r'^review review--with-sidebar')})
			#print(filteredreviews)
			for r in filteredreviews:
				author = ''
				authorid = ''
				friends = ''
				numberOfReviews = ''
				rating = ''
				review = ''
				date = ''
				author = r.find('span', {'class':'user-display-name'}).getText()
				author=author.strip()
				print("Author",author)
				
				authorid = r.find('span', {'class':'user-display-name'})['data-hovercard-id']
				authorid=authorid.strip()
				print("Author id",authorid)
				friends = r.find('li', {'class':'friend-count responsive-small-display-inline-block'}).getText()
				friends=str(friends).replace("\\n","")
				friends=friends.strip()
				print("Friend",friends)
				rating = r.find('li', {'class':'review-count responsive-small-display-inline-block'}).getText()
				rating = str(rating).replace("\\n","")
				rating=rating.strip()
				print(rating)
				review = r.find('p', {'lang':'en'}).getText()
				review=review.strip()
				print(review)
				date = r.find('span', {'class':'rating-qualifier'}).getText()
				date=str(date).replace("\\n","")
				date=date.strip()
				print(date)
				data.append([business["id"],business["name"],ad,business["phone"],business["location"]["zip_code"],business["location"]["state"],business["review_count"],business["rating"],author,date,review,"FAKE"])
	except:
		pass
	print(data)

	print ("Writing data to output file")
	with open('dataset1.csv','w',newline='',encoding="utf-8") as fp:
		fieldnames= ['ID','NAME','ADDRESS','PHONE','ZIPCODE','STATE','REVIEWCOUNT','RATING','AUTHOR','DATE','REVIEW','LABEL']
		writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
		writer.writerow(fieldnames)
		for m in data:
			writer.writerow(m)
#process()
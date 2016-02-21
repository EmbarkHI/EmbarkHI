from flask import render_template, url_for, request
from Kronos import app
import requests, demjson
from urllib2 import urlopen
import json, datetime, xlrd

international = False
departDate = datetime.date.today()
arriveDate = departDate
category = 0 #tourism =1, getaway = 0
loc = [28, 77]
cities = []
countries = []
itineary = ""
categoryArray = []
chosen = dict()
costDict = {}

@app.route('/')
def home(): #Function to render index page
	global home, homeCountry, homeTown
	return render_template("index.html")

@app.route('/query1.html', methods =['GET','POST'])
def query1():#Rendering Page 2 
	return render_template("query1.html")

@app.route('/query2.html', methods =['GET','POST'])
def query2():#POST request for Departure & Return Dates, Category Preference. Rendering Page 3
	global departDate, arriveDate, category
	if request.method== "POST":
		departDate = (request.form["depDate"])
		arriveDate = (request.form["retDate"])
		if request.form["catPref"] == "gtW":
			category = 0
		else:
			category = 1
		print category
	return render_template("query2.html")

@app.route('/result1.html', methods =['GET','POST'])
def result1():#POST request for Query 2. Rendering result. 
	#print request.method
	global home, homeCountry, homeTown, category, international, budget, chosenCities, chosenBudgets, categoryArray, cities, countries, validCities
	print category, "Hello"
	if request.method== "POST":
		budget = (int)(request.form["budget"])
		if request.form["trvlPref"] == "doM":
			international = False
		else:
			international = True
	home = getplace(loc[0],loc[1])
	homeCountry = home[1]
	homeTown = home[0]
	define_list()
	categoryArray = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0]
	choice_category()
	print validCities
	validCities = choice_international()
	print validCities
	choice_budget()
	chosenCities = chosen.keys()
	chosenBudgets = chosen.values()
	blocks = ["block"]*4		
	while len(chosenCities) != 4:
		chosenCities += [0]
		chosenBudgets += [0]
	for j in range(len(chosenCities)):
		if chosenCities[j]==0:
			blocks[j] = "none"
	for i in range(len(chosenCities)):
		chosenBudgets[i] = chosen[chosenCities[i]]
	for l in range(len(chosenCities)):
		k = chosenCities[l]
		if isinstance(k, str):
			chosenCities[l] = k.lower()
	return render_template("result1.html",city1=chosenCities[0],city2=chosenCities[1],city3=chosenCities[2],city4=chosenCities[3],budget1=chosenBudgets[0],budget2=chosenBudgets[1],budget3=chosenBudgets[2],budget4=chosenBudgets[3],show1=blocks[0],show2=blocks[1],show3=blocks[2],show4=blocks[3])

@app.route('/result2.html', methods =['GET','POST'])
def result2():#POST request for a specific city. Rendering final result. 
	if request.method == "POST":
		print "Hello"
		print (type)(request.form)
		print request.form
		cname = (request.form["city"])
		print cname
	pointsOfInterest(cname)
	print "PoI success"
	print costDict
	return render_template("result2.html",city=cname.title(),flightc=(costDict[cname.title()])[0],hotelc=(costDict[cname.title()])[1],p1wikiurl=links[0],p1mainimg=images[0],p1name=titles[0],p2wikiurl=links[1],p2mainimg=images[1],p2name=titles[1],p3wikiurl=links[2],p3mainimg=images[2],p3name=titles[2])

@app.route('/final1.html', methods =['GET','POST'])
def final():
	return render_template("final1.html")
	
def define_list():#Matching cities to countries; Assigning every city as valid. 
	global categoryArray, cities, countries, validCities
	cities = ["Abu Dhabi","Antalya","Atlanta","Auckland","Baku","Bangkok","Barcelona","Beijing","Berlin","Bilbao","Birmingham","Bratislava","Bucharest","Budapest","Cairo","Cape Town","Chennai","Chiang Mai","Chicago","Christchurch","Copenhagen","Denpasar","Doha","Dubai","Dublin","Edinburgh","Florence","Glasgow","Graz","Guangzhou","Hamburg","Hangzhou","Hanoi","Helsinki","Ho Chi Minh City","Honolulu","Indianapolis","Innsbruck","Iowa City","Jaipur","Jakarta","Jerusalem","Kiev","Kolkata","Krakow","Las Vegas","Lima","Linz","Lisbon","Liverpool","London","Los Angeles","Lyon","Madrid","Manama","Manchester","Manila","Marseille","Mecca","Melbourne","Mexico City","Milan","Monaco","Montreal","Moscow","Mumbai","Munich","Nairobi","Nanjing","New Delhi","New York","Newcastle upon Tyne","Nice","Orlando","Oslo","Oxford","Paris","Prague","Reims","Reykjavik","Riyadh","Rome","San Diego","San Francisco","San Jose","Seattle","Seoul","Shanghai","Shenzhen","Singapore","Sofia","Stockholm","Sydney","Tallinn","Tel Aviv","Toronto","Turku","Vancouver","Vienna","Warsaw","Washington","Zaragoza","Zurich"]
	countries = ["United Arab Emirates","Turkey","United States","New Zealand","Azerbaijan","Thailand","Spain","China","Germany","Spain","United Kingdom","Slovakia","Romania","Hungary","Egypt","South Africa","India","Thailand","United States","New Zealand","Denmark","Indonesia","Qatar","United Arab Emirates","Ireland","United Kingdom","Italy","United Kingdom","Austria","China","Germany","China","Vietnam","Finland","Vietnam","United States","United States","Austria","United States","India","Indonesia","Israel","Ukraine","India","Poland","United States","Peru","Austria","Portugal","United Kingdom","United Kingdom","United States","France","Spain","Bahrain","United Kingdom","Philippines","France","Saudi Arabia","Australia","Mexico","Italy","Monaco","Canada","Russia","India","Germany","Kenya","China","India","United States","United Kingdom","France","United States","Norway","United Kingdom","France","Czech Republic","France","Iceland","Saudi Arabia","Italy","United States","United States","United States","United States","South Korea","China","Hong Kong","Singapore","Bulgaria","Sweden","Australia","Estonia","Israel","Canada","Finland","Canada","Austria","Poland","United States","Spain","Switzerland"]
	validCities = [1]*len(cities)
	#To define the countries array
	"""for i in range(len(l)):
		s = country_from_city(l[i])
		countries += [s]
	"""

def country_from_city(city):#Ran only once to get co-ordinates of each city using POI
	city = city.replace (" ", "%20")
	r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&city_name={0}'.format(city))
	the_page = r.text
	the_page = demjson.decode(the_page)
	while ("status" in the_page):
		r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&city_name={0}'.format(city))
		the_page = r.text
		the_page = demjson.decode(the_page)
	l1 = the_page["points_of_interest"]
	i = l1[0]
	location = [(i["location"]).values()[0],(i["location"]).values()[2]]
	return (getplace(location[0],location[1]))[1]

def getplace(lat, lon):#Function to get country of cities using co-ordinates. Ran only once for each city.
	url = "http://maps.googleapis.com/maps/api/geocode/json?"
	url += "latlng=%s,%s&sensor=false" % (lat, lon)
	v = urlopen(url).read()
	j = json.loads(v)
	components = j['results'][0]['address_components']
	country = town = None
	for c in components:
	    if "country" in c['types']:
	        country = c['long_name']
	    if "postal_town" in c['types']:
	        town = c['long_name']
	return town, country

def choice_international():#Narrowing list of valid cities using choice of travel
	global validCities
	for i in range(len(countries)):
		if (international):
			if (homeCountry==countries[i]):
				validCities[i] = 0
				print countries[i], i, 
		else:
			if (homeCountry!=countries[i]):
				validCities[i] = 0
	return validCities

def choice_budget():
	global chosen, validCities, costDict
	travelcosts = dict()
	lattitude = (str)(loc[0])
	longitude = (str)(loc[1])
	re = requests.get('https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&latitude=' + (lattitude) + '&longitude=' + (longitude))
	page = re.text
	page = demjson.decode(page)
	d_code = (page[0])["airport"]
	x = len(countries)
	if international:
		x = 15
	for i in range(x):
			if (1==validCities[i]):
				city = cities[i].replace (" ", "%20")
				print city
				re = requests.get("https://api.sandbox.amadeus.com/v1.2/airports/autocomplete?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&term={0}".format(city)) 
				page = re.text
				page = demjson.decode(page)
				if page == []:
					validCities[i] = 0
				else:
					a_code = page[0]["value"]
					re = requests.get("https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&origin="+d_code+"&destination="+a_code+"&departure_date="+str(departDate)+"&return_date="+str(arriveDate))
					page = re.text
					page = demjson.decode(page)
					if ("status" in page):
						validCities[i] = 0
					else:
						global travelcosts, costDict
						results = page["results"]
						price = results[0]["fare"]["total_price"]
						airfare = (float)(price)

						re = requests.get("https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&location="+a_code+"&check_in="+str(departDate)+"&check_out="+str(arriveDate))
						page = re.text
						page = demjson.decode(page)
						results = page["results"]
						if results == []:
							validCities[i] = 0
						else:
							price = results[0]["total_price"]["amount"]
							stayfare = (float)(price)
							costDict[cities[i]] = [airfare,stayfare]
							total_cost = airfare+stayfare
							travelcosts[total_cost]= cities[i]
	costs = travelcosts.keys()
	costs.sort()
	costs = budget_helper(costs, budget)
	for i in range(4):
		if i>=len(travelcosts):
			chosen[0]=0
		else:
			chosen[travelcosts[costs[i]]] = costs[i]
	print travelcosts
	print costDict

def budget_helper(costs_local, budget):
	Aroundbudget = [0]*4
	if (len(costs_local) <4):
		return costs_local
	else:	
		for i in range(len(costs_local)):
			if (( costs_local[i] < budget) and (i!= (len(costs_local)-1))):
				pass
			elif (costs_local[i] >= budget and i!= (len(costs_local)-1)):
				if (i-3 >=0):
					Aroundbudget[0] = costs_local[i-3]
					Aroundbudget[1] = costs_local[i-2]
					Aroundbudget[2] = costs_local[i-1]
					Aroundbudget[3] = costs_local[i]
					return Aroundbudget
				elif (i-2 >=0) :
					Aroundbudget[0] = costs_local[i-2]
					Aroundbudget[1] = costs_local[i-1]
					Aroundbudget[2] = costs_local[i]
					Aroundbudget[4] = costs_local[i+1]
					return Aroundbudget
				elif (i-1 >= 0):
					Aroundbudget[0] = costs_local[i-1]
					Aroundbudget[1] = costs_local[i]
					Aroundbudget[2] = costs_local[i+1]
					Aroundbudget[3] = costs_local[i+2]
					return Aroundbudget
				else:
					Aroundbudget[0] = costs_local[i]
					Aroundbudget[1] = costs_local[i+1]
					Aroundbudget[2] = costs_local[i+2]
					Aroundbudget[3] = costs_local[i+3]
					return Aroundbudget
			else:
				Aroundbudget[0] = costs_local[i-3]
				Aroundbudget[1] = costs_local[i-2]
				Aroundbudget[2] = costs_local[i-1]
				Aroundbudget[3] = costs_local[i]
				return Aroundbudget
 
def choice_category():
	global validCities
	for i in range(len(countries)):
			if (category!=categoryArray[i]):
				print "True", i
				validCities[i] = 0 

def read_categories(filename):
	book = xlrd.open_workbook(filename)
	sheet = book.sheet_by_index(0)
	urban = []
	tourism = []
	final = [0]*(len(cities))
	for j in range(45):
		tourism.append(sheet.cell_value(rowx=j,colx=2))
	for k in range(len(cities)):
		if cities[k] in tourism:
			final[k] = 1
	
	return final

def pointsOfInterest(city):
	global images, titles, links
	city_name = city.replace(" ","%20")
	r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&city_name='+city_name)
	print r.url
	the_page = r.text
	the_page = demjson.decode(the_page)
	while ("status" in the_page):
		r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey=WCC0Tn8fJ5hScMw7NTDDAAkjydFLOYTf&city_name={0}'.format(city_name))
		the_page = r.text
		the_page = demjson.decode(the_page)
	l1 = the_page["points_of_interest"]
	print l1
	images = [] 
	titles = []
	links = []
	for i in range(3):
		images.append(l1[i]["main_image"])
		titles.append(l1[i]["title"])
		links.append(l1[i]["details"]["wiki_page_link"])
	
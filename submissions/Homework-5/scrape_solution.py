#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import logging
import requests
import urllib2
from BeautifulSoup import BeautifulSoup



log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(loghandler)

base_url = "http://www.tripadvisor.com/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"


parser = argparse.ArgumentParser(description='Scrape tripadvisor')
parser.add_argument('-datadir', type=str,
                    help='Directory to store raw html files',
                    default="data/")
parser.add_argument('-state', type=str,
                    help='State for which the hotel data is required.',
                    required=True)
parser.add_argument('-city', type=str,
                    help='City for which the hotel data is required.',
                    required=True)
args = parser.parse_args()


def get_city_page(city, state):
    """ Returns the URL of the list of the hotels in a city. Corresponds to
    STEP 1 & 2 of the slides.

    Parameters
    ----------
    city : str

    state : str


    Returns
    -------
    url : str
        The relative link to the website with the hotels list.

    """
    # Build the request URL
    url = base_url + "city=" + city + "&state=" + state
    # Request the HTML page
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    with open(os.path.join(args.datadir, city + '-tourism-page.html'), "w") as h:
        h.write(html)

    # Use BeautifulSoup to extract the url for the list of hotels in
    # the city and state we are interested in.

    # For example in this case we need to get the following href
    # <li class="hotels twoLines">
    # <a href="/Hotels-g60745-Boston_Massachusetts-Hotels.html" data-trk="hotels_nav">...</a>
    soup = BeautifulSoup(html)
    li = soup.find("li", {"class": "hotels twoLines"})
    city_url = li.find('a', href=True)
    return city_url['href']


def get_hotellist_page(city_url, page_count):
    """ Returns the hotel list HTML. The URL of the list is the result of
    get_city_page(). Also, saves a copy of the HTML to the disk. Corresponds to
    STEP 3 of the slides.

    Parameters
    ----------
    city_url : str
        The relative URL of the hotels in the city we are interested in.
    page_count : int
        The page that we want to fetch. Used for keeping track of our progress.

    Returns
    -------
    html : str
        The HTML of the page with the list of the hotels.
    """
    url = base_url + city_url
    # Sleep 2 sec before starting a new http request
    time.sleep(2)
    # Request page
    headers = { 'User-Agent' : user_agent }
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    # Save the webpage
    with open(os.path.join(args.datadir, args.city + '-hotelist-' + str(page_count) + '.html'), "w") as h:
        h.write(html)
    return html


def parse_hotellist_page(html):
    """Parses the website with the hotel list and prints the hotel name, the
    number of stars and the number of reviews it has. If there is a next page
    in the hotel list, it returns a list to that page. Otherwise, it exits the
    script. Corresponds to STEP 4 of the slides.

    Parameters
    ----------
    html : str
        The HTML of the website with the hotel list.

    Returns
    -------
    URL : str
        If there is a next page, return a relative link to this page.
        Otherwise, exit the script.
    """
    soup = BeautifulSoup(html)
    # Extract hotel name, star rating and number of reviews
    hotel_boxes = soup.findAll('div', {'class' :'listing wrap reasoning_v5_wrap jfy_listing p13n_imperfect'})
    if not hotel_boxes:
        log.info("#################################### Option 2 ######################################")
        hotel_boxes = soup.findAll('div', {'class' :'listing_info jfy'})
    if not hotel_boxes:
        log.info("#################################### Option 3 ######################################")
        hotel_boxes = soup.findAll('div', {'class' :'listing easyClear  p13n_imperfect'})

    for hotel_box in hotel_boxes:
        hotel_name = hotel_box.find("a", {"target" : "_blank"}).find(text=True)
        log.info("Hotel name: %s" % hotel_name.strip())

        stars = hotel_box.find("img", {"class" : "sprite-ratings"})
        if stars:
            log.info("Stars: %s" % stars['alt'].split()[0])

        num_reviews = hotel_box.find("span", {'class': "more"}).findAll(text=True)
        if num_reviews:
            log.info("Number of reviews: %s " % [x for x in num_reviews if "review" in x][0].strip())

    # Get next URL page if exists, otherwise exit

	'''
	
	stopper = 0
	i = 0
	storage_array = []
	while (stopper == 0):
		if i == 0:
			first_page = urllib2.urlopen("http://www.tripadvisor.com/Hotels-g60745-Boston_Massachusetts-Hotels.html")
			soup = BeautifulSoup(first_page)
			storage_array.append(first_page.read())
			i = i + 30
		else:
			page_html = "-oa%s-" (str(i))
			html_page = urllib2.urlopen("http://www.tripadvisor.com/Hotels-g60745-%sBoston_Massachusetts-Hotels.html" (page_html))
			if html_page != first_page:
				soup = BeautifulSoup(html_page)
				storage_array.append(html_page.read())
				i = i + 30
			else:
				log.info("We reached last page")
				stopper = 1
		return storage_array
		
		

	
	div = soup.find("div", {"class" : "pgLinks"})
	storage_array = []
	hrefs = div.findAll('a', href= True)
	for href in hrefs:
		if href.find(
		
	
	
	html_page = urllib2.urlopen("http://www.yourwebsite.com")
	soup = BeautifulSoup(html_page)
	for link in soup.findAll('a'):
    print link.get('href')
	

	for i in range(1,1000):
		for href in hrefs:			
			if href.find(text = True) == str(i):
				log.info("Next url is %s" % href['href'])
				storage_array.append(href['href'])
			elif href.find(text = True) == '&laquo;':
				log.info("We reached first page")
				storage_array.append(href['href'])
			elif href.find(text = True) == '&raquo;':
				log.info("We reached last page")
				storage_array.append(href['href'])
		return storage_array
			


	for 
	
	http://www.tripadvisor.com/Hotels-g60745-Boston_Massachusetts-Hotels.html
	
	http://www.tripadvisor.com/Hotels-g60745-oa30-Boston_Massachusetts-Hotels.html#ACCOM_OVERVIEW
	
	http://www.tripadvisor.com/Hotels-g60745-oa60-Boston_Massachusetts-Hotels.html#ACCOM_OVERVIEW
	
	# check if this is the last page
    if div.find('span', {'class' : 'nav next disabled'}):
        log.info("We reached last page")
        sys.exit()
    # If not, return the url to the next page
    hrefs = div.findAll('a', href= True)
    for href in hrefs:
        if href.find(text = True) == 'Next':
            log.info("Next url is %s" % href['href'])
            return href['href']
	
	
	

	stopper = 0
	i = 30
	div = soup.find("div", {"class" : "pgLinks"})
	hrefs = div.findAll('a', href= True)
    for href in hrefs:
		while (stopper == 0):
			if href.find == "http://www.tripadvisor.com/Hotels-g60745-Boston_Massachusetts-Hotels.html":
				log.info("Next url is %s" % href['href'])
				return href['href']
			else:
				page_html = "-oa%s-" % (str(i))
				if href.find == "http://www.tripadvisor.com/Hotels-g60745-%sBoston_Massachusetts-Hotels.html" % (page_html):
					i = i + 30
					log.info("Next url is %s" % href['href'])
					return href['href']
				else:
					log.info("We reached last page")
					stopper = 1
				
	'''

	
	div = soup.find("div", {"class" : "pgLinks"})
	hrefs = div.findAll('a', href= True)
    for href in hrefs:
		if "-oa%s-" % str(i) in href['href']:
			log.info("Next url is %s" % href['href'])
			print href['href']
			print i,i,i,i,i,i,i,i,i,i,i,i
			return href['href']
		else:
			if href.find(text = True) == "&laquo":
				print i,i,i,i,i,i,i,i,i,i,i,i
				return href['href']
				log.info("We reached last page")
				stopper = 1
		
			


	
if __name__ == "__main__":
    # Get current directory
    current_dir = os.getcwd()
    # Create datadir if does not exist
    if not os.path.exists(os.path.join(current_dir, args.datadir)):
        os.makedirs(os.path.join(current_dir, args.datadir))

    # Get URL to obtaint the list of hotels in a specific city
	city_url = get_city_page(args.city, args.state)
	c=0
	i=0
	stopper = 0
	while(True and stopper == 0):
		c +=1
		i +=30
		html = get_hotellist_page(city_url,c)
		city_url = parse_hotellist_page(html)


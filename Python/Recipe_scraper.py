from recipe_scrapers import scrape_me
import urllib.request
import re
import requests # to get image from the web
import shutil # to save it locally
import os

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
scraper = scrape_me('https://www.cookingclassy.com/white-chicken-chili/')


#print(scraper.title())
scraper.total_time()
scraper.yields()
#print(scraper.ingredients())
#print(scraper.instructions())
#print(scraper.image())
scraper.host()
#print(scraper.links())
scraper.nutrients()  # if available


def get_image(url, title):
  
    pathname_tuple = os.path.splitext(url)
    file_extension = pathname_tuple[1]
    
    ## Set up the image URL and filename
    image_url = url
    filename = "/Users/Alexander/Documents/Thonny_Projects/Recipe_book/" + str(title) + str(file_extension)
    filename = filename.replace(" ", "")
    

    
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')
get_image(scraper.image(), scraper.title())
#urllib.request.urlretrieve(str(scraper.image), "/Users/Alexander/Documents/Thonny_Projects/Recipe_book/random.jpg")

    
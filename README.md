# IceCreamFinal
SI206 final project 

● Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

This program uses the yelp fusion API. To get an API key you must create an account and then create an app using this site: https://www.yelp.com/developers/v3/manage_app. To use the keys, you must enter them into a file titled secrets.py (which is included in the git ignore file).

Format for secrets.py

Client_ID = ' '

APIKey = ' '

● Any other information needed to run the program (e.g., pointer to getting started info for plotly)
First, create a plotly account. Here is a useful page for getting started with plotly: https://plot.ly/python/getting-started/. Make sure to follow the installation directions. Also, you must initialize for online plotting and set your credentials. Use the following code and enter your individual username and api_key:
import plotly
plotly.tools.set_credentials_file(username='DemoAccount', api_key='lr1c37zw81')


● Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.

def init_db() is an important function as it initializes information into the database. The data comes from two sources, one table is from the yelp API key, the other is from scraping the yelp website. 

def scrape() both scrapes and crawls the yelp pages for the names of ice cream store and addresses.

def interation() is the interactive part of the project that allows users to enter input and gives different results according to user input. 

class store creates a list of instances of different ice cream store locations and is used to get store and address data



● Brief user guide, including how to run the program and how to choose presentation options.
To run the program, run the icecream.py file in terminal. The program will ask to enter a city and gives a model (ex: ann arbor, mi). It is important to follow this syntax. Next, the program asks how you would like to view your results? Options include rating, distance, or view all graphs. The user can also at any time enter exit to leave the program. If the user chooses rating, the search results will be sorted according to rating. If the user chooses distance, the search results will be sorted according to distance. Next, the user must select a store to receive an address. Again, syntax must be correct, as the program states enter the store exactly as seen. The program spits out the address for the according store. On the other hand, if the user enters "view all graphs", four plotly pages will be pulled up in the browser. The first graph is a bar graph that displays store distances in km, the second graph is also a bar graph that displaysnthe number of reviews (review count) for each store. The third graph is a pie chart that displays the percentage of restaurants in the search that are 5 stars, 4.5 stars, 4 stars, etc. Lastly, the fourth graph takes the top store from each search result (rating vs. review count) and compares them using a double bar graph. 





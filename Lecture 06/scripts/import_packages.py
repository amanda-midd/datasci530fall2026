
#------------------- IMPORT PACKAGES FOR DATA PROCESSING ----------------------#

# Manage datasets
import pandas as pd

# Work with time data
import time 

# Conduct HTTP requests
import requests

# Construct tree structure of HTML data
import html5lib

# Parse HTML data obtained from scraping
from bs4 import BeautifulSoup

# Import webdriver for chrome
from webdriver_manager.chrome import ChromeDriverManager


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Automate navigating within browser (SELENIUM)
#------ Key: Manage keys
#------ Select: Obtain features from website
#------ WebDriverWait: Add wait times implicitly
#------ By: Use common information locator strategies
#------ EC and Options: Browser configuration
#------ remote.command: Check whether browser is active

from selenium import webdriver #to automate the navigating within the browser
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver.support.ui     import Select
from selenium.webdriver.support.ui     import WebDriverWait 
from selenium.webdriver.common.by      import By
from selenium.webdriver.support        import expected_conditions as EC
from selenium.webdriver.chrome.options import Options #to use properties of the chrome webbrowser
from selenium.webdriver.remote.command import Command # Use to check whether the web driver is active
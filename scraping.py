import re
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.chrome.options import Options
import sys

def scrape_website(starting_index, num_pages, openNeeded):

    file = open("CUScrape.csv", "w", newline='')
    writer = csv.writer(file)
    writer.writerow(["Class Code", "Class Name", "Credit Hours", "Class Description", "Instructor(s)", "Registration Requirements"])

    if openNeeded:
        print("opening browser")
        url = 'https://classes.colorado.edu'
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome()
        browser.get(url)

        browser.find_element("xpath",'//*[@id="crit-camp"]/option[9]').click()
        browser.find_element("xpath",'//*[@id="search-button"]').click()

        time.sleep(3)

    for i in range(starting_index, starting_index + num_pages):
        # time.sleep(random.uniform(1.0, 3.0))  # Random delay between requests
        # if i == 48 or i == 49:
        #     i = 60
        #     print("skipped over 48 and 49", i)
        print(f"Page {i}")
        try:
            link = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/main/div[2]/div/div[3]/div[{i}]/a"))
            )

            # Scroll to the element
            actions = ActionChains(browser)
            actions.move_to_element(link).perform()

            time.sleep(1)  # Adding a delay to make sure element is ready to be clicked

            # Relocate the element after the delay
            link = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/main/div[2]/div/div[3]/div[{i}]/a"))
            )

            link.click()
        except:
            print(f"Page {i} did not load")
            continue

        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        try:
            codes = soup.find("div", attrs={"class": "dtl-course-code"}).text
        except AttributeError:
            codes = ""
            print(f"Did not find codes on page {i}")

        try:
            names = soup.find("div", attrs={"class": "text col-8 detail-title text--huge"}).text
        except AttributeError:
            names = ""
            print(f"Did not find names on page {i}")

        try:
            credithours_divs = soup.find("div", attrs={"class": "text detail-hours_text"}).text
            if credithours_divs != "Credit Hours: Varies by section":
                credithours = re.findall("\d+", credithours_divs)
                ch = int(credithours[0])
            else:
                ch = credithours_divs
        except AttributeError:
            ch = ""
            print(f"Did not find credit hours on page {i}")

        try:
            description_divs = soup.find('div', attrs = {"class" : "section--description"})
            descriptions = description_divs.find('div', attrs = {"class" : "section__content"}).text
        except AttributeError:
            descriptions = ""
            print(f"Did not find descriptions on page {i}")

        try:
            instructor_divs = soup.find('div', attrs = {"class" : "section section--instructor_info_html"})
            instructors = instructor_divs.find('div', attrs = {"class" : "section__content"}).text
        except AttributeError:
            instructors = ""
            print(f"Did not find instructors on page {i}")

        try:
            regreq_divs = soup.find('div', attrs = {"class" : "section section--restrict_info"})
            regreqs = regreq_divs.find('div', attrs = {"class" : "section__content"}).text
        except AttributeError:
            regreqs = ""
            print(f"Did not find registration requirements on page {i}")

        writer.writerow([codes, names, ch, descriptions, instructors, regreqs])
        with open('page_number.txt', 'w') as f:
            f.write(str(i))
        
    file.close()
    browser.quit()
    
# if __name__ == "__main__":
#     # Convert the command-line arguments to integers and pass them to the function
#     start_index = int(sys.argv[1])
#     num_pages = int(sys.argv[2])
#     openNeeded = sys.argv[3].lower() in ('yes', 'true', 't', '1')
#     scrape_website(start_index, num_pages, openNeeded)

scrape_website(1, 3545, True)
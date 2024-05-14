from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.firefox.service import Service
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import json
import csv
import tkinter as tk
from tkinter import messagebox
import subprocess

def scrape_data():
    url = "https://platform.arkhamintelligence.com/explorer/entity/binance"

    geckodriver_path = "C:\\Users\\franc\\Repositories\\arkham-scraper\\geckodriver_win32.exe"
    firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    # Start the BrowserMob Proxy server
    bmp_path = "C:\\Users\\franc\\Repositories\\arkham-scraper\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy"
    server = Server(bmp_path)
    server.start()
    proxy = server.create_proxy()

    # Set up Selenium with FirefoxOptions
    options = FirefoxOptions()
    proxy_settings = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy.proxy,
        'sslProxy': proxy.proxy
    })
    options.proxy = proxy_settings
    options.binary_location = firefox_binary_path

    # Initialize WebDriver with FirefoxOptions
    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)

    # Start capturing network traffic
    proxy.new_har("arkham", options={'captureHeaders': True, 'captureContent': True})

    # Navigate to the page
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # Click on the OUTFLOW tab
    outflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", outflow_tab)
    time.sleep(1)  # Wait for any overlay to disappear
    driver.execute_script("arguments[0].click();", outflow_tab)

    try: 
        for page_number in range(1, 4):
            # Click on the page input field and enter the page number
            page_input_xpath = '/html/body/div[1]/div/div[3]/div[1]/a[1]/div/div[2]/div[1]/div[4]/h1/div/div/div/div/div/input'
            page_input = wait.until(EC.visibility_of_element_located((By.XPATH, page_input_xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", page_input)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", page_input)
            page_input.clear()
            page_input.send_keys(str(page_number))
            page_input.send_keys(Keys.ENTER)

            time.sleep(2)

    except TimeoutException:
        print("Timed out waiting for elements to appear.")

    try:
        # Retrieve the captured network traffic
        time.sleep(10)  # Wait for the network traffic to be captured
        traffic = proxy.har
        
        for i in range(3):  # Iterate 625 times
            offset = i * 16
            request_url = f'https://api.arkhamintelligence.com/transfers?sortKey=time&sortDir=desc&limit=16&offset={offset}&flow=out&base=binance&usdGte=0.1'
            # found = False
            for entry in traffic['log']['entries']:
                if request_url in entry['request']['url']:
                    found = True
                    print(f"Found request at offset {offset}: {entry['request']['url']}")
                    # Check if 'text' attribute exists in the response content
                    if 'text' in entry['response']['content']:
                        print(entry['response']['content']['text'])
                    else:
                        print("Response content does not contain text.")
            # if not found:
            #     print(f"No request found for offset {offset}")

        # log the found network traffic to a json file
        with open("demo.json", "w", encoding='utf-8') as f:
            json.dump(traffic, f, ensure_ascii=False, indent=4)
        # if there's no error, print success message
        print("Scraping successful!")

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        server.stop()
        # time.sleep(120)  # Delay for 2 minutes
def write_transfers_to_csv(json_file_path, csv_file_path):
    # Open the JSON file and load the data
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        # Navigate to the nested 'transfers' data
        entries = data['log']['entries']
        transfers_data = []
        for entry in entries:
            # Check if the response content type is JSON
            if ('response' in entry and 
                'content' in entry['response'] and 
                'mimeType' in entry['response']['content'] and 
                entry['response']['content']['mimeType'] == "application/json; charset=UTF-8" and
                'text' in entry['response']['content']):
                
                content_text = entry['response']['content']['text']
                try:
                    # Parse the JSON data from the text
                    content_data = json.loads(content_text)
                    # Ensure content_data is a dictionary and 'transfers' is a key in it
                    if isinstance(content_data, dict) and 'transfers' in content_data:
                        for transfer in content_data['transfers']:
                            to_address = transfer['toAddress']['address']
                            chain = transfer['chain']
                            # entity = transfer['fromAddress']['arkhamEntity']['name']
                            # Check if 'arkhamEntity' key exists
                            if 'arkhamEntity' in transfer['fromAddress']:
                                entity = transfer['fromAddress']['arkhamEntity']['name']
                            else:
                                entity = 'Unknown'
                            transfers_data.append({
                                'address': to_address,
                                'chain': chain,
                                'entity': entity,
                                'category': 'exchange'
                            })
                except json.JSONDecodeError:
                    continue
    
    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)
        
        # Check if there are transfers in the data
        if transfers_data:
            # Write the header row
            headers = ['address', 'chain', 'entity', 'category']
            csv_writer.writerow(headers)
            
            # Write data rows
            for transfer in transfers_data:
                csv_writer.writerow([transfer['address'], transfer['chain'], transfer['entity'], transfer['category']])

def open_csv_file(csv_file_path):
    root = tk.Tk()
    root.withdraw()

    result = messagebox.askquestion('Open File', 'Open output CSV file?')

    if result == 'yes':
        subprocess.call(["start", csv_file_path], shell=True)

# Main execution
if __name__ == "__main__":
    # download_folder = "/Users/fjnervida/Documents"  # path of download folder
    # download_folder = "C:\\Users\\franc\\Repositories\\arkham-scraper"
    # Path to the JSON file
    json_file_path = 'C:\\Users\\franc\\Repositories\\arkham-scraper\\demo.json'
    # Path to the output CSV file
    csv_file_path = 'C:\\Users\\franc\\Repositories\\arkham-scraper\\output_clean.csv'
    scrape_data()
    write_transfers_to_csv(json_file_path, csv_file_path)
    open_csv_file(csv_file_path)
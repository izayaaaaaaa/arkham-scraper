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
import json
from selenium.webdriver.common.keys import Keys

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
        for page_number in range(1, 3):
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
            found = False
            for entry in traffic['log']['entries']:
                if request_url in entry['request']['url']:
                    found = True
                    print(f"Found request at offset {offset}: {entry['request']['url']}")
                    # Check if 'text' attribute exists in the response content
                    if 'text' in entry['response']['content']:
                        print(entry['response']['content']['text'])
                    else:
                        print("Response content does not contain text.")
            if not found:
                print(f"No request found for offset {offset}")

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


# Main execution
if __name__ == "__main__":
    # download_folder = "/Users/fjnervida/Documents"  # path of download folder
    # download_folder = "C:\\Users\\franc\\Repositories\\arkham-scraper"
    scrape_data()
# Code 1

from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import os
import glob
import csv
import time
import subprocess
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Scraper part
def scrape_data1():
    url = "https://platform.arkhamintelligence.com/explorer/entity/binance"

    # driver = webdriver.Firefox()  # mac path
    geckodriver_path = "C:\\Users\\franc\\Repositories\\arkham-scraper\\geckodriver_win32.exe"
    # Specify the path to Firefox (optional)
    firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    # Set up Firefox options
    options = Options()
    options.binary_location = firefox_binary_path
    # Initialize the driver with the specified options and service
    driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # pagination & download, filter post download
    try:
        for page_number in range(1, 101):
            # outflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))
            # driver.execute_script("arguments[0].scrollIntoView(true);", outflow_tab)
            # time.sleep(1)  # Wait for any overlay to disappear
            # driver.execute_script("arguments[0].click();", outflow_tab)

            # page_input_xpath = '/html/body/div[1]/div/div[3]/div[1]/a[1]/div/div[2]/div[1]/div[4]/h1/div/div/div/div/div/input'
            # page_input = wait.until(EC.visibility_of_element_located((By.XPATH, page_input_xpath)))
            # driver.execute_script("arguments[0].scrollIntoView(true);", page_input)
            # time.sleep(1)
            # driver.execute_script("arguments[0].click();", page_input)
            # page_input.clear()
            # page_input.send_keys(str(page_number))
            # page_input.send_keys(Keys.ENTER)

            # time.sleep(2)

            # download_button_xpath = '/html/body/div[1]/div/div[3]/div[1]/a[1]/div/div[1]/div[2]/svg[2]'
            # download_button = wait.until(EC.visibility_of_element_located((By.XPATH, download_button_xpath)))
            download_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//svg[contains(@d, "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4")]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", download_button)
            time.sleep(1)

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # driver.quit()
        time.sleep(120)  # Delay for 2 minutes

# -------------- 
# Code 2
# --------------

# Scraper part
# def scrape_data2():
#     url = "https://platform.arkhamintelligence.com/explorer/entity/coinbase"
#     driver = webdriver.Firefox()  # mac path
#     # driver = webdriver.Firefox(executable_path="C:/geckodriver.exe") # windows path
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)

#     # outflow & filter to tron
#     try:
#         inflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))

#         # Scroll into view
#         driver.execute_script("arguments[0].scrollIntoView(true);", inflow_tab)
#         time.sleep(1)  # Wait for any overlay to disappear

#         # Try clicking using JavaScript
#         driver.execute_script("arguments[0].click();", inflow_tab)

#         # Click the filter button
#         filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Transactions_filterButtonContainer__WGF88 svg")))
#         filter_button.click()
        
#         # Wait for filter options to appear and click on polygon
#         polygon_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ETHEREUM')]")))
#         polygon_option.click()

#     except TimeoutException:
#         print("Timed out waiting for the inflow tab to be clickable.")
#         driver.quit()
#         return

#     # pagination & download
#     try:
#         for page_number in range(1, 101):
#             wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")))
#             page_input = driver.find_element(By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")
#             page_input.click()
#             page_input.clear()
#             page_input.send_keys(str(page_number))
#             page_input.send_keys(Keys.ENTER)

#             time.sleep(2)

#             container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Transactions_csvButtonsContainer__dhv_J")))
#             svgs = container.find_elements(By.TAG_NAME, "svg")
#             if len(svgs) > 1:
#                 svgs[1].click()
#             else:
#                 print(f"Second SVG element not found on page {page_number}.")
            
#             # Wait for the download to complete
#             time.sleep(1)

#     except TimeoutException:
#         print("Timed out waiting for elements to appear.")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#     finally:
#         driver.quit()
#         time.sleep(120)  # Delay for 2 minutes

# -------------- 
# Code 3
# --------------   

# Scraper part
# def scrape_data3():
    url = "https://platform.arkhamintelligence.com/explorer/entity/okx"
    driver = webdriver.Firefox()  # mac path
    # driver = webdriver.Firefox(executable_path="C:/geckodriver.exe") # windows path
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # outflow & filter to tron
    try:
        inflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", inflow_tab)
        time.sleep(1)  # Wait for any overlay to disappear

        # Try clicking using JavaScript
        driver.execute_script("arguments[0].click();", inflow_tab)

        # Click the filter button
        filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Transactions_filterButtonContainer__WGF88 svg")))
        filter_button.click()
        
        # Wait for filter options to appear and click on polygon
        polygon_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ETHEREUM')]")))
        polygon_option.click()

    except TimeoutException:
        print("Timed out waiting for the inflow tab to be clickable.")
        driver.quit()
        return

    # pagination & download
    try:
        for page_number in range(1, 101):
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")))
            page_input = driver.find_element(By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")
            page_input.click()
            page_input.clear()
            page_input.send_keys(str(page_number))
            page_input.send_keys(Keys.ENTER)

            time.sleep(2)

            container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Transactions_csvButtonsContainer__dhv_J")))
            svgs = container.find_elements(By.TAG_NAME, "svg")
            if len(svgs) > 1:
                svgs[1].click()
            else:
                print(f"Second SVG element not found on page {page_number}.")
            
            # Wait for the download to complete
            time.sleep(1)

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        time.sleep(120)  # Delay for 2 minutes


# -------------- 
# Code 4
# --------------   

# Scraper part
# def scrape_data4():
    url = "https://platform.arkhamintelligence.com/explorer/entity/kraken"
    driver = webdriver.Firefox()  # mac path
    # driver = webdriver.Firefox(executable_path="C:/geckodriver.exe") # windows path
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # outflow & filter to tron
    try:
        inflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", inflow_tab)
        time.sleep(1)  # Wait for any overlay to disappear

        # Try clicking using JavaScript
        driver.execute_script("arguments[0].click();", inflow_tab)

        # Click the filter button
        filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Transactions_filterButtonContainer__WGF88 svg")))
        filter_button.click()
        
        # Wait for filter options to appear and click on polygon
        polygon_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ETHEREUM')]")))
        polygon_option.click()

    except TimeoutException:
        print("Timed out waiting for the inflow tab to be clickable.")
        driver.quit()
        return

    # pagination & download
    try:
        for page_number in range(1, 101):
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")))
            page_input = driver.find_element(By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")
            page_input.click()
            page_input.clear()
            page_input.send_keys(str(page_number))
            page_input.send_keys(Keys.ENTER)

            time.sleep(2)

            container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Transactions_csvButtonsContainer__dhv_J")))
            svgs = container.find_elements(By.TAG_NAME, "svg")
            if len(svgs) > 1:
                svgs[1].click()
            else:
                print(f"Second SVG element not found on page {page_number}.")
            
            # Wait for the download to complete
            time.sleep(1)

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        time.sleep(120)  # Delay for 2 minutes

# -------------- 
# Code 5
# --------------   

# Scraper part
# def scrape_data5():
    url = "https://platform.arkhamintelligence.com/explorer/entity/mexc"
    driver = webdriver.Firefox()  # mac path
    # driver = webdriver.Firefox(executable_path="C:/geckodriver.exe") # windows path
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # outflow & filter to tron
    try:
        inflow_tab = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='OUTFLOW']")))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", inflow_tab)
        time.sleep(1)  # Wait for any overlay to disappear

        # Try clicking using JavaScript
        driver.execute_script("arguments[0].click();", inflow_tab)

        # Click the filter button
        filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Transactions_filterButtonContainer__WGF88 svg")))
        filter_button.click()
        
        # Wait for filter options to appear and click on polygon
        polygon_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ETHEREUM')]")))
        polygon_option.click()

    except TimeoutException:
        print("Timed out waiting for the inflow tab to be clickable.")
        driver.quit()
        return

    # pagination & download
    try:
        for page_number in range(1, 101):
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")))
            page_input = driver.find_element(By.CSS_SELECTOR, "input.Input_input__IL5XS.Input_smallClosed__vW4aj")
            page_input.click()
            page_input.clear()
            page_input.send_keys(str(page_number))
            page_input.send_keys(Keys.ENTER)

            time.sleep(2)

            container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Transactions_csvButtonsContainer__dhv_J")))
            svgs = container.find_elements(By.TAG_NAME, "svg")
            if len(svgs) > 1:
                svgs[1].click()
            else:
                print(f"Second SVG element not found on page {page_number}.")
            
            # Wait for the download to complete
            time.sleep(1)

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

# Main execution
if __name__ == "__main__":
    # download_folder = "/Users/fjnervida/Documents"  # path of download folder
    download_folder = "C:\\Users\\franc\\Repositories\\arkham-scraper"
    scrape_data1()
    
    # scrape_data2()   

    # scrape_data3()   

    # scrape_data4()

    # scrape_data5()

    #Code 6 cleaning

# output_rows = []
# download_path = 'C:\\Users\\franc\\Repositories\\arkham-scraper'
# output_folder = 'C:\\Users\\franc\\Repositories\\arkham-scraper'
# csv_files = glob.glob(os.path.join(download_path, 'arkham_txns*.csv'))

# for csv_file in csv_files:
#     with open(csv_file, 'r') as f:
#         reader = csv.reader(f)
#         header = next(reader)
#         from_address_idx = header.index('fromAddress')  
#         from_label_idx = header.index('fromLabel')
#         to_address_idx = header.index('toAddress')
#         to_label_idx = header.index('toLabel')
#         chain_idx = header.index('chain')
        
#         for row in reader:
#             address = row[from_address_idx] 
#             label = row[from_label_idx].split()[0] # Take the first word only
#             if address != label:
#                 output_rows.append([address, label, row[chain_idx], 'exchange'])
            
#             address = row[to_address_idx]
#             label = row[to_label_idx].split()[0] # Take the first word only
#             if address != label:
#                 output_rows.append([address, label, row[chain_idx], 'exchange'])
                
# # output_rows = set(map(tuple, output_rows))

# # if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
    
# output_csv = os.path.join(output_folder, 'consolidatedarkham.csv')
# with open(output_csv, 'w') as f:
#     writer = csv.writer(f)  
#     writer.writerow(['address', 'entity', 'chain', 'category']) 
#     writer.writerows(output_rows)
    
# Delete original csv files
# for csv_file in csv_files:
#     os.remove(csv_file)

# Added popup code

# root = tk.Tk()
# root.withdraw()

# row_count = len(output_rows) 

# messagebox.showinfo('Complete', 'Finished consolidating CSVs! {} rows written. Output file: {}'.format(row_count, output_csv))

# result = messagebox.askquestion('Open File', 'Open output CSV file?')

# if result == 'yes':
#     import subprocess
#     subprocess.call(["open", output_csv])
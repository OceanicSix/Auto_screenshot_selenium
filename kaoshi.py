import selenium
from PIL import Image
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#define param here
login_url="https://www.kaoshibao.com/login/"
username_xpath="/html/body/div[3]/div/div/section/div[2]/div[2]/div[2]/form/div/div[1]/div/div/div/input"
pass_xpath="/html/body/div[3]/div/div/section/div[2]/div[2]/div[2]/form/div/div[2]/div/div/div[1]/input"
login_button_xpath="/html/body/div[3]/div/div/section/div[2]/div[2]/div[2]/form/div/div[3]/button"
username="username"
password="password"
success_indication_xpath="/html/body/div[3]/div/section/section/main/div/div/div[1]/div[4]/div/div[2]/p[3]/img"


target_url="https://www.kaoshibao.com/online/?paperId=9527983&practice=&modal=1&is_recite=&qtype=&text=%E9%80%82%E4%B8%AD&sequence=0&kid=&is_collect=1&difficulty=2&is_vip_paper=0"
target_xpath="/html/body/div[3]/div/div/section/div[2]/div[1]/div[2]"


#Switch to headless 
chrome_options=Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080') 
driver=webdriver.Chrome("/usr/bin/chromedriver",options=chrome_options)


#driver=webdriver.Chrome("/usr/bin/chromedriver")
#driver.maximize_window()


driver.get(login_url)

username_input = driver.find_element(By.XPATH,username_xpath)  # Replace with the actual ID of the username input field
password_input = driver.find_element(By.XPATH,pass_xpath)  # Replace with the actual ID of the password input field

username_input.send_keys(username)  # Replace 'your_username' with your actual username
password_input.send_keys(password)  # Replace 'your_password' with your actual password

# Submit the login form
login_button = driver.find_element(By.XPATH,login_button_xpath)  # Replace with the actual ID of the login button
login_button.click()

#Wait login to complete
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH,success_indication_xpath)))


# Get page 
driver.get(target_url)


#check pop up window
try:
    popup_cancel_button= driver.find_element(By.XPATH,"/html/body/div[4]/div/div[3]/button[1]")
    if popup_cancel_button:
        popup_cancel_button.click()
finally:

                                            
    # change disply mode to show answers

    checkbox= driver.find_element(By.XPATH,"/html/body/div[3]/div/div/section/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/span[2]/div")
    html_text=checkbox.text
    if "is-checked" not in html_text:
        checkbox.click()


    # Download image
    element=driver.find_element(By.XPATH,target_xpath)
    location = element.location
    size = element.size

    x = location['x']
    y = location['y']
    width = size['width']
    height = size['height']
    driver.save_screenshot(f'''full_screenshort/full_screenshot1.png''')
    full_screenshot = Image.open(f'''full_screenshort/full_screenshot1.png''')
    partial_screenshot = full_screenshot.crop((x, y, x + width, y + height))
    partial_screenshot.save(f'''partial_screenshot/partial_screenshot1.png''')

    for seq in range (2,474):
        question=driver.find_element(By.XPATH,f'''/html/body/div[3]/div/div/section/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/span[{seq}]''')
        question.click()
        time.sleep(1)
        driver.save_screenshot(f'''full_screenshort/full_screenshot{seq}.png''')
        full_screenshot = Image.open(f'''full_screenshort/full_screenshot{seq}.png''')
        partial_screenshot = full_screenshot.crop((x, y, x + width, y + height))
        partial_screenshot.save(f'''partial_screenshot/partial_screenshot{seq}.png''')


    input("Press Enter to quit...")
    # Quit the driver
    driver.quit()


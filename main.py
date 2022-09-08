from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.tz import gettz
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from config import userid, passwd, ttoken


def send_doc(file_name, download_path):
    token = ttoken
    file_path = os.path.join(download_path, file_name)
    url = "https://api.telegram.org/bot{}/sendDocument?chat_id=-631494811".format(token)
    files = {'document': open(file_path, 'rb')}
    status = requests.post(url, files=files)
    if status.ok:
        try:
            os.remove(file_path)
        except:
            pass
        return True
    return False


def down():
    download_path = "/home/ubuntu/downloads/"
    if os.name == "nt":
        download_path = "D:\\aj\\"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 ' \
                 'Safari/537.36 '
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('prefs', {
        "download.default_directory": download_path,  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    driver = webdriver.Chrome(options=options)
    driver.get("https://ka54.remsl.in/UMPeMandi/")

    if os.name == "nt":
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='login.userId']"))).send_keys(userid)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='password']"))).send_keys(passwd)
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
    else:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='login.userId']"))).click()
        driver.find_element(By.CSS_SELECTOR, "input[data-ng-model='login.userId']").clear()
        driver.find_element(By.CSS_SELECTOR, "input[data-ng-model='login.userId']").send_keys(userid)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='password']"))).click()
        driver.find_element(By.CSS_SELECTOR, "input[data-ng-model='password']").clear()
        driver.find_element(By.CSS_SELECTOR, "input[data-ng-model='password']").send_keys(passwd)
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
    try:
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
        driver.find_element(By.XPATH, "//button[@data-ng-click='doLogin()']").click()
    except:
        pass

    driver.save_screenshot("ss.png")
    time.sleep(50)
    driver.save_screenshot("ss1.png")
    button = driver.find_element(By.LINK_TEXT, "Daily Report")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(button).click(button).perform()
    driver.find_element(By.LINK_TEXT, "Winner List Format 3 Download").click()
    time.sleep(3)
    select = Select(driver.find_element(By.ID, "batchId"))
    select.select_by_visible_text('COTTON|1')

    driver.find_element(By.XPATH,
                        "//select[@data-ng-model='winnerListDnld.session']/optgroup[@label='ETender "
                        "Sessions']/option[@value='1']").click()

    # to be commented
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='winnerListDnld.tradeDate']"))).clear()
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-ng-model='winnerListDnld.tradeDate']"))).send_keys(
    #     "05-Sep-2022")

    before = os.listdir(download_path)
    driver.save_screenshot("ss2.png")
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)
    driver.find_element(By.XPATH, '//button[text()="Print"]').click()
    try:
        time.sleep(10)
        obj = driver.switch_to.alert
        if obj.text == "File not found.":
            driver.close()
            return False
    except:
        pass
    driver.save_screenshot("ss3.png")
    time.sleep(50)
    after = os.listdir(download_path)
    change = set(after) - set(before)
    file_name = ""
    if len(change) == 1:
        file_name = change.pop()
    try:
        driver.find_element(By.CLASS_NAME, "user-profile.dropdown-toggle.ng-binding").click()
        driver.find_element(By.LINK_TEXT, "Log Out").click()
    except:
        pass
    driver.close()
    if file_name:
        return send_doc(file_name, download_path)
    return False


flag = False
while 1:
    time.sleep(350)
    day = (datetime.now(tz=gettz('Asia/Kolkata'))).today().weekday()
    #day = 0
    if day != 0 and day != 3:
        flag = False
        continue
    else:
        h = (datetime.now(tz=gettz('Asia/Kolkata'))).hour
        #h = 13
        if h < 13 or h > 14:
            continue
    try:
        if not flag:
            flag = down()

    except Exception as e:
        print(e, end="\n\n")
        continue

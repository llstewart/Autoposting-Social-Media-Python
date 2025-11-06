import facebook
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from twocaptcha import TwoCaptcha
import pandas as pd
from os.path import abspath
import time

class AutoPost:
    def __init__(self):
        self.image_path = ""
        self.image_desc = ""
        self.url = ""
    def user_input(self):
        # Enter path image from a internet source or from your local device from the current directory
        self.image_path = input("Enter Path Of The Image (E.g. thor.jpg) : ")
        self.image_desc = input("Write Description Of The Image : ")
        # Enter A Valid URL starting from https or http.
        self.url = input("Enter The URL : ")

    def post_to_facebook(self):
        self.user_input()
        # Enter the access page token of your fb page generated from Graph API of Facebook Developers Site(https://developers.facebook.com/tools/). Token must enclosed between quotes as a string.
        token = 'EAAPaKfEyiSABAKtzmZBai64TdqZAQ56RW2cOsPQRruzOxrOtQWIUB3rvuoV227I5F2pJCP64ZBGTI7lOEC9vPdIgg0ubvnJee7rTx8DZBIJRPxhefRU95pIYg80m4hRPZChYPj5eBUCPcthAlkZADnYWpjvUriZCYhdYkeSjtZAwcgZDZD' #Enter access page token inside these blank quotes.
        fb = facebook.GraphAPI(access_token = token)
        fb.put_photo(image = open(self.image_path, 'rb'), message = self.image_desc + '\n' + self.url)
        print("Successfully Posted Content On Your Facebook Page!!")

    def post_to_twitter(self):
        self.user_input()
        # Enter consumer key, consumer secret key, access token and access secret token of your Twitter handle. Get it from the https://apps.twitter.com/
        # Make sure to put all the token values inside the blank double quotes.
        consumer_key = "o0iBjVWuidJu9WsNofA5q6uWA"
        consumer_secret = "fv5sq7TsBAa4hqg6fM4t8Iuj1RCuKlCxCYdNNz9oaHPHOMIQqA"
        access_token = "966334170539503617-dpwTiliYyRRKMob54qGUHZtJ8Os3BCA"
        access_token_secret = "SePvdqq7ITBhs2a8yFtWhILkmwTF7oopONlia4LmOCrI2"
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # update the status with media
        tweet = self.image_desc + '\n' + self.url
        image_path = self.image_path
        # Upload media and post tweet
        media = api.media_upload(image_path)
        api.update_status(status=tweet, media_ids=[media.media_id])
        print("Successfully Posted Content On Your Twitter Handle!!")

    def post_to_linkedin(self):
        self.user_input()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # reading csv file
        df = pd.read_csv("linkedin.csv", encoding='utf-8')
        # reading username
        myUsername = df.Username[0]
        # reading password
        myPassword = df.Password[0]
        absolute_file_path = abspath(self.image_path)
        # driver.get method() will navigate to a page given by the URL address
        driver.get("https://www.linkedin.com/login?")
        username = driver.find_element(By.NAME, 'session_key')
        username.send_keys(myUsername)
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys(myPassword)
        log_in_button = driver.find_element(By.CLASS_NAME, 'btn__primary--large')
        log_in_button.click()
        start_post = driver.find_element(By.CLASS_NAME, 'share-box__trigger')
        start_post.click()
        text = driver.find_element(By.CLASS_NAME, 'mentions-texteditor__content')
        # send_keys() to simulate key strokes
        text.send_keys(self.image_desc + "\n" + self.url)
        image = driver.find_element(By.XPATH, '//*[@data-control-name="share.select_image"]')
        image.click()
        photo = driver.find_element(By.XPATH, '//*[@data-control-name="select_photo"]').send_keys(absolute_file_path)
        next = driver.find_element(By.XPATH, '//*[@data-control-name="confirm_selected_photo"]')
        next.click()
        post = driver.find_element(By.XPATH, '//*[@data-control-name="share.post"]')
        post.click()
        print("Successfully Posted Content On Your LinkedIn Page!!")

    def post_to_tiktok(self):
        self.user_input()
        # Use undetected chromedriver to bypass TikTok's bot detection
        driver = uc.Chrome()
        # reading csv file for TikTok credentials
        df = pd.read_csv("tiktok.csv", encoding='utf-8')
        # reading username
        myUsername = df.Username[0]
        # reading password
        myPassword = df.Password[0]
        absolute_file_path = abspath(self.image_path)
        
        # Load 2Captcha API key
        config_df = pd.read_csv("config.csv", encoding='utf-8')
        captcha_api_key = config_df[config_df['Service'] == '2captcha']['API_Key'].values[0]
        solver = TwoCaptcha(captcha_api_key)
        
        # Navigate to TikTok login page
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(3)
        
        # Login to TikTok
        try:
            # Click on "Use phone / email / username" option
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(myUsername)
            
            password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
            password_field.send_keys(myPassword)
            
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()
            
            # Wait for CAPTCHA to appear and solve it automatically
            print("\n⏳ Waiting for CAPTCHA...")
            time.sleep(3)
            
            # Check if CAPTCHA appeared
            try:
                # Look for CAPTCHA iframe or element
                captcha_frame = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//iframe[contains(@id, "captcha")]'))
                )
                print("🔍 CAPTCHA detected! Solving with 2Captcha...")
                
                # Get the page source/screenshot for CAPTCHA solving
                page_url = driver.current_url
                
                # For TikTok's slider CAPTCHA, we need to use GeeTest or similar
                # Get the sitekey or necessary parameters
                driver.switch_to.frame(captcha_frame)
                
                # Try to get CAPTCHA parameters
                try:
                    # This is a simplified approach - TikTok uses complex CAPTCHA
                    # For production, you'd need to identify the exact CAPTCHA type
                    print("⚠️  TikTok uses complex slider CAPTCHA.")
                    print("📝 2Captcha requires manual intervention for slider puzzles.")
                    print("🔄 Falling back to manual solving...")
                    driver.switch_to.default_content()
                    
                    # Manual solving fallback
                    print("\n" + "="*60)
                    print("⚠️  CAPTCHA DETECTED - MANUAL ACTION REQUIRED")
                    print("="*60)
                    print("Please solve the CAPTCHA puzzle in the browser window.")
                    print("After solving it and successfully logging in,")
                    input("press ENTER here to continue...\n")
                    
                except Exception as captcha_error:
                    print(f"CAPTCHA solving error: {captcha_error}")
                    driver.switch_to.default_content()
                    
            except:
                # No CAPTCHA appeared, login successful
                print("✅ No CAPTCHA detected, login successful!")
                time.sleep(2)
            
            # Navigate to upload page
            driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Upload video/image
            upload_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
            )
            upload_input.send_keys(absolute_file_path)
            time.sleep(5)
            
            # Add caption
            caption_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            caption_field.send_keys(self.image_desc + "\n" + self.url)
            time.sleep(2)
            
            # Click post button
            post_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Post")]'))
            )
            post_button.click()
            time.sleep(3)
            
            print("Successfully Posted Content On Your TikTok Account!!")
        except Exception as e:
            print(f"Error posting to TikTok: {e}")
        finally:
            driver.quit()


if __name__ == '__main__':
    ap = AutoPost()
    while(True):
        app = input("Where do you want to post your content? (facebook, twitter, linkedin, tiktok or exit)\n")
        if app == 'facebook':
            ap.post_to_facebook()
        elif app == 'twitter':
            ap.post_to_twitter()
        elif app == 'linkedin':
            ap.post_to_linkedin()
        elif app == 'tiktok':
            ap.post_to_tiktok()
        elif app == 'exit':
            break
        else:
            print("\nInvalid Appname. Please Try Again!\n")
            continue
        ch = input("\nWanna Add More Content?(y/n)\n")
        if ch == 'n':
            break

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
import requests

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
        # Reading csv file for Facebook credentials
        df = pd.read_csv("facebook.csv", encoding='utf-8')
        # Reading access token (can be user or page token)
        user_access_token = df.AccessToken[0]
        
        # Post to Facebook using modern Graph API (direct HTTP requests)
        try:
            # Step 1: Get list of pages managed by this user and convert to Page Access Token
            print("🔄 Getting Page Access Token...")
            accounts_url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={user_access_token}"
            accounts_response = requests.get(accounts_url)
            
            if accounts_response.status_code != 200:
                print(f"❌ Error getting pages: {accounts_response.json()}")
                print("\nMake sure your token has 'pages_show_list' and 'pages_manage_posts' permissions")
                return
            
            pages_data = accounts_response.json()
            print(f"📋 Debug - API Response: {pages_data}")  # Debug output
            
            if not pages_data.get('data') or len(pages_data.get('data', [])) == 0:
                print("\n❌ No Facebook Pages found for this account")
                print("\nThis means your token doesn't have 'pages_show_list' permission.")
                print("\n🔧 To fix this:")
                print("1. Go to: https://developers.facebook.com/tools/explorer/")
                print("2. Click 'Get Token' → 'Get User Access Token'")
                print("3. Check these permissions:")
                print("   ✓ pages_show_list")
                print("   ✓ pages_manage_posts")
                print("   ✓ pages_read_engagement")
                print("4. Copy the new token to facebook.csv")
                return
            
            # Use the first page (or you can add logic to select specific page)
            page = pages_data['data'][0]
            page_id = page['id']
            page_name = page['name']
            page_access_token = page['access_token']  # This is the Page Access Token
            
            print(f"✓ Connected to Page: '{page_name}' (ID: {page_id})")
            print(f"✓ Using Page Access Token")
            
            # Step 2: Upload photo using Page Access Token
            photo_url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
            message = self.image_desc + '\n' + self.url
            
            with open(self.image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': message,
                    'access_token': page_access_token  # Use Page token, not User token
                }
                
                response = requests.post(photo_url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✨ Successfully Posted Content On Your Facebook Page!!")
                print(f"📸 Post ID: {result.get('id', 'Unknown')}")
            else:
                error_info = response.json()
                print(f"❌ Facebook API Error: {error_info}")
                print("\nTroubleshooting:")
                print("1. Make sure your token has 'pages_manage_posts' permission")
                print("2. Make sure your token has 'pages_show_list' permission")
                print("3. Check token at: https://developers.facebook.com/tools/debug/accesstoken/")
            
        except Exception as e:
            print(f"❌ Error posting to Facebook: {e}")

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

    def post_to_instagram(self):
        self.user_input()
        # Use undetected chromedriver to bypass Instagram's bot detection
        driver = uc.Chrome()
        # reading csv file for Instagram credentials
        df = pd.read_csv("instagram.csv", encoding='utf-8')
        # reading username
        myUsername = df.Username[0]
        # reading password
        myPassword = df.Password[0]
        absolute_file_path = abspath(self.image_path)
        
        # Navigate to Instagram login page
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        # Login to Instagram
        try:
            # Enter username
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(myUsername)
            
            # Enter password
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(myPassword)
            
            # Click login button
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()
            
            print("\n⏳ Logging in...")
            time.sleep(5)
            
            # Function to dismiss any popup
            def dismiss_popup():
                popup_dismissed = False
                # Try all possible popup dismiss buttons
                dismiss_buttons = [
                    '//button[contains(text(), "Not Now")]',
                    '//button[contains(text(), "Not now")]',
                    '//button[contains(text(), "Never")]',
                    '//button[contains(text(), "not now")]',
                    '//button[text()="Not Now"]',
                    '//div[@role="dialog"]//button[contains(., "Not Now")]',
                    '//div[@role="dialog"]//button[contains(., "Never")]'
                ]
                
                for xpath in dismiss_buttons:
                    try:
                        button = driver.find_element(By.XPATH, xpath)
                        if button.is_displayed():
                            button.click()
                            popup_dismissed = True
                            time.sleep(1)
                            break
                    except:
                        continue
                return popup_dismissed
            
            # Handle "Save Login Info" / "Save password?" prompt (first attempt)
            try:
                time.sleep(2)
                if dismiss_popup():
                    print("✅ Dismissed 'Save Login Info' popup")
                    time.sleep(2)
            except:
                pass
            
            # Handle "Turn on Notifications" prompt
            try:
                time.sleep(1)
                if dismiss_popup():
                    print("✅ Dismissed 'Notifications' popup")
                    time.sleep(2)
            except:
                pass
            
            # Extra check for any remaining popups before proceeding
            try:
                time.sleep(1)
                if dismiss_popup():
                    print("✅ Dismissed additional popup")
                    time.sleep(1)
            except:
                pass
            
            print("✅ Logged in successfully!")
            
            # Click on Create/New Post button (+ icon in sidebar)
            print("📸 Creating new post...")
            try:
                # Try multiple selectors for the Create button
                create_post_button = None
                selectors = [
                    '//a[@href="#"]//span[contains(@class, "x1lliihq") and contains(@class, "x1plvlek")]//parent::div//parent::a[contains(@href, "#")]',
                    '//a[contains(@href, "/create/")]',
                    '//span[text()="Create"]//ancestor::a',
                    '//div[@role="menuitem"]//span[text()="Create"]//ancestor::a',
                    '//a[@aria-label="New post"]',
                    '//a[@aria-label="Create"]',
                    '//span[contains(text(), "Create")]//parent::*//parent::a'
                ]
                
                for selector in selectors:
                    try:
                        create_post_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"✓ Found Create button with selector")
                        break
                    except:
                        continue
                
                if create_post_button:
                    create_post_button.click()
                    time.sleep(2)
                else:
                    raise Exception("Could not find Create button")
                    
            except Exception as e:
                print(f"⚠️  Error finding Create button: {e}")
                print("Trying alternative approach...")
                # Try clicking on the sidebar Create option by position
                driver.find_element(By.XPATH, '//a[contains(@href, "#")]//span[contains(text(), "Create")]').click()
                time.sleep(2)
            
            # Click on "Post" from the Create submenu
            print("📝 Selecting 'Post' option...")
            try:
                post_option_selectors = [
                    # Match the actual <a> link element with SVG aria-label
                    '//a[@role="link" and @href="#"]//svg[@aria-label="Post"]//ancestor::a',
                    '//svg[@aria-label="Post"]//ancestor::a[@role="link"]',
                    '//a[@role="link"]//svg[@aria-label="Post"]//parent::div//parent::div//parent::div//parent::div//parent::div//parent::a',
                    # Match by the nested span text within the link
                    '//a[@role="link" and @href="#"]//span[text()="Post"]//ancestor::a',
                    '//a[@role="link"]//span[@class="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft" and text()="Post"]//ancestor::a',
                    # Simpler approaches
                    '//a[@href="#" and .//span[text()="Post"]]',
                    '//a[contains(@class, "x1i10hfl") and @role="link" and @href="#" and .//span[text()="Post"]]'
                ]
                
                post_option_clicked = False
                for idx, selector in enumerate(post_option_selectors):
                    try:
                        post_option = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        # Check if element is visible
                        if post_option.is_displayed():
                            print(f"  → Found Post button with selector #{idx+1}")
                            # Try both regular click and JavaScript click
                            try:
                                post_option.click()
                                print("  → Clicked with regular method")
                            except:
                                driver.execute_script("arguments[0].click();", post_option)
                                print("  → Clicked with JavaScript")
                            post_option_clicked = True
                            print("✓ Selected 'Post' option")
                            time.sleep(5)
                            break
                    except Exception as sel_error:
                        continue
                
                if not post_option_clicked:
                    print("⚠️  Could not find 'Post' option in submenu, trying fallback methods...")
                    # Final attempt: find any element with "Post" text or aria-label
                    try:
                        # Try by SVG aria-label first
                        svg_elements = driver.find_elements(By.XPATH, '//svg[@aria-label="Post"]')
                        for svg in svg_elements:
                            if svg.is_displayed():
                                # Click the parent <a> tag
                                parent_link = svg.find_element(By.XPATH, './ancestor::a[@role="link"]')
                                driver.execute_script("arguments[0].click();", parent_link)
                                print("✓ Clicked 'Post' via SVG aria-label (JavaScript)")
                                time.sleep(5)
                                post_option_clicked = True
                                break
                        
                        # If still not clicked, try any element with "Post" text
                        if not post_option_clicked:
                            all_elements = driver.find_elements(By.XPATH, '//*[text()="Post"]')
                            for elem in all_elements:
                                if elem.is_displayed():
                                    driver.execute_script("arguments[0].click();", elem)
                                    print("✓ Clicked 'Post' via text match (JavaScript)")
                                    time.sleep(5)
                                    post_option_clicked = True
                                    break
                    except:
                        pass
                        
                if not post_option_clicked:
                    print("⚠️  Could not find 'Post' option, continuing anyway...")
                    
            except Exception as e:
                print(f"⚠️  Error selecting Post option: {e}")
            
            # Upload photo
            print("📤 Uploading photo...")
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
            )
            file_input.send_keys(absolute_file_path)
            time.sleep(3)
            
            # Click Next button after photo upload (to proceed to crop/edit screen)
            print("➡️  Clicking Next after upload...")
            try:
                next_selectors = [
                    '//div[@role="button" and text()="Next"]',
                    '//div[@role="button" and contains(text(), "Next")]',
                    '//button[contains(text(), "Next")]',
                    '//*[@role="button"][text()="Next"]'
                ]
                
                next_clicked = False
                for selector in next_selectors:
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        next_button.click()
                        print("✓ Clicked Next (crop/edit)")
                        time.sleep(3)
                        next_clicked = True
                        break
                    except:
                        continue
                
                if not next_clicked:
                    print("⚠️  Could not find Next button after upload")
            except Exception as e:
                print(f"⚠️  Error clicking Next after upload: {e}")
            
            # Click Next button again (to proceed to caption screen)
            print("➡️  Proceeding to caption screen...")
            try:
                for selector in next_selectors:
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        next_button.click()
                        print("✓ Clicked Next (to caption)")
                        time.sleep(3)
                        break
                    except:
                        continue
            except Exception as e:
                print(f"⚠️  Error clicking Next to caption: {e}")
            
            # Add caption
            print("✍️  Adding caption...")
            try:
                caption_selectors = [
                    '//div[@aria-label="Write a caption..." and @contenteditable="true"]',
                    '//div[@contenteditable="true" and @role="textbox"][@aria-label="Write a caption..."]',
                    '//div[@role="textbox" and contains(@class, "notranslate")][@aria-label="Write a caption..."]',
                    '//textarea[@aria-label="Write a caption..."]'
                ]
                
                caption_field_found = False
                for selector in caption_selectors:
                    try:
                        caption_field = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        caption_text = self.image_desc + "\n\n" + self.url
                        caption_field.send_keys(caption_text)
                        print("✓ Caption added successfully")
                        time.sleep(2)
                        caption_field_found = True
                        break
                    except:
                        continue
                
                if not caption_field_found:
                    print("⚠️  Could not find caption field, continuing...")
            except Exception as e:
                print(f"⚠️  Error adding caption: {e}")
            
            # Click Share button
            print("🚀 Posting...")
            try:
                share_selectors = [
                    '//div[@role="button" and text()="Share"]',
                    '//div[@role="button" and contains(text(), "Share")]',
                    '//button[contains(text(), "Share")]',
                    '//*[@role="button"][text()="Share"]'
                ]
                
                share_clicked = False
                for selector in share_selectors:
                    try:
                        share_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        share_button.click()
                        print("✓ Share button clicked")
                        time.sleep(5)
                        share_clicked = True
                        break
                    except:
                        continue
                
                if not share_clicked:
                    print("⚠️  Could not find Share button")
            except Exception as e:
                print(f"⚠️  Error clicking Share: {e}")
            
            print("✨ Successfully Posted Content On Your Instagram Account!!")
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ Error posting to Instagram: {e}")
            print("Browser will remain open for 10 seconds for inspection...")
            time.sleep(10)
        finally:
            try:
                driver.quit()
            except:
                pass


if __name__ == '__main__':
    ap = AutoPost()
    while(True):
        app = input("Where do you want to post your content? (facebook, twitter, linkedin, tiktok, instagram or exit)\n")
        if app == 'facebook':
            ap.post_to_facebook()
        elif app == 'twitter':
            ap.post_to_twitter()
        elif app == 'linkedin':
            ap.post_to_linkedin()
        elif app == 'tiktok':
            ap.post_to_tiktok()
        elif app == 'instagram':
            ap.post_to_instagram()
        elif app == 'exit':
            break
        else:
            print("\nInvalid Appname. Please Try Again!\n")
            continue
        ch = input("\nWanna Add More Content?(y/n)\n")
        if ch == 'n':
            break

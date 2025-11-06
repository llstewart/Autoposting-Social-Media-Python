# Autoposting-Social-Media-Python
This is a python based autoposting social media script where one can automatically post images, text captions, an url directly to their social media accounts (Facebook, Twitter, LinkedIn, TikTok, and Instagram) by just running the python script.

# Getting Started
First things first, let's install all the necessary modules for this project.<br>
Just clone this repository and open it in command line. Then type pip install -r requirements.txt and hit enter. All the required modules will be installed and ready to use.<br>
Or Do it manually for each of the module:<br>
1) Facebook API - pip install facebook-sdk<br>
2) Twitter API - pip install tweepy<br>
3) Selenium - pip install selenium<br>
4) Pandas - pip install pandas<br><br>

<strong>PERFECT!!</strong>

# How It Works?
Okay for testing purposes I have already added access tokens for my dummy facebook, twitter pages. So you don't need to worry about that but it's better if you do it on your own account/pages. For LinkedIn and TikTok, we use Selenium with Chrome driver so make sure that you have downloaded chrome driver from here https://chromedriver.chromium.org/downloads.<br>

**Configuration:**<br>
- **Facebook & Twitter**: Update access tokens in `autopost.py`<br>
- **LinkedIn**: Update credentials in `linkedin.csv`<br>
- **TikTok**: Update credentials in `tiktok.csv` (note: must support video uploads)<br>
- **Instagram**: Update credentials in `instagram.csv`<br>
- **CAPTCHA Solving**: Add your 2Captcha API key in `config.csv` (get it from https://2captcha.com)<br>

**Setting up 2Captcha (for TikTok automation):**<br>
1. Sign up at https://2captcha.com<br>
2. Get your API key from the dashboard<br>
3. Add funds to your account (~$1-3 per 1000 CAPTCHAs)<br>
4. Update `config.csv` with your API key<br>

Now you are good to go. Just run the autopost.py script and play around with different functions. Type python autopost.py in command line and hit enter.<br><br>

# Supported Platforms
This script supports posting to the following platforms:<br>
* **Facebook** - Uses Facebook Graph API<br>
* **Twitter** - Uses Tweepy API<br>
* **LinkedIn** - Uses Selenium automation<br>
* **TikTok** - Uses Selenium automation with 2Captcha<br>
* **Instagram** - Uses Selenium automation<br>

# Test Pages
Demo facebook and twitter pages:<br>
* Facebook : https://www.facebook.com/codingrdx/ <br>
* Twitter : https://twitter.com/venom_rdx


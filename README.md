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
All platform credentials are stored in CSV files for easy configuration. For LinkedIn, TikTok, and Instagram, we use Selenium with undetected Chrome driver for automation. For Twitter, you'll need to update the API credentials directly in `autopost.py`.<br>

**Configuration:**<br>
- **Facebook**: Update your page access token in `facebook.csv` (get it from https://developers.facebook.com/tools/)<br>
- **Twitter**: Update API credentials in `autopost.py`<br>
- **LinkedIn**: Update credentials in `linkedin.csv`<br>
- **TikTok**: Update credentials in `tiktok.csv`<br>
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


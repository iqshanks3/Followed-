import requests
import time
import random
import sys
import os
import subprocess
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class UltimateRealBooster:
    def __init__(self, username, platform, service_type, amount=100):
        self.username = username
        self.platform = platform
        self.service_type = service_type
        self.amount = amount
        self.driver = None
        self.results = []
        self.session = requests.Session()
        self.platform_names_ar = {
            "instagram": "انستقرام",
            "tiktok": "تيك توك",
            "facebook": "فيسبوك",
            "snapchat": "سناب شات",
            "telegram": "تليكرام",
            "twitter": "تويتر X"
        }
        self.service_names_ar = {
            "followers": "متابعين",
            "likes": "إعجابات",
            "views": "مشاهدات",
            "comments": "تعليقات"
        }
        self.setup_session()
        
    def setup_session(self):
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def get_chrome_version(self):
        system = platform.system()
        try:
            if system == "Linux":
                result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            elif system == "Windows":
                result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], capture_output=True, text=True)
            else:
                result = subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], capture_output=True, text=True)
            version = result.stdout.strip().split()[-1]
            return version.split('.')[0]
        except:
            return "120"
            
    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--headless=new')
            
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            chrome_version = self.get_chrome_version()
            chrome_driver_paths = [
                "/usr/bin/chromedriver",
                "/usr/local/bin/chromedriver",
                "./chromedriver",
                "/usr/lib/chromium-browser/chromedriver"
            ]
            
            service = None
            for path in chrome_driver_paths:
                if os.path.exists(path):
                    service = Service(path)
                    break
            
            if not service:
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    service = Service(ChromeDriverManager().install())
                except:
                    print("⚠️ Installing chromedriver...")
                    os.system("apt-get update && apt-get install -y chromium-chromedriver")
                    service = Service("/usr/lib/chromium-browser/chromedriver")
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"⚠️ Driver error: {e}")
            return False
            
    def countdown_timer(self, seconds=10):
        print(f"\n⏰ جاري تجهيز الرشق خلال {seconds} ثواني...")
        for i in range(seconds, 0, -1):
            bar_length = 30
            filled = int(bar_length * (seconds - i) / seconds)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r[{bar}] {i} ثانية متبقية", end="", flush=True)
            time.sleep(1)
        print("\n🚀 بدء الرشق الآن!\n")
        
    def send_free_site_request(self, site):
        try:
            self.driver.get(site["url"])
            wait = WebDriverWait(self.driver, 25)
            time.sleep(random.uniform(5, 10))
            
            input_selectors = [
                (By.NAME, "username"), (By.ID, "username"), (By.NAME, "user"),
                (By.ID, "user"), (By.CSS_SELECTOR, "input[placeholder*='username']"),
                (By.CSS_SELECTOR, "input[placeholder*='Username']"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]
            
            username_field = None
            for by, selector in input_selectors:
                try:
                    username_field = wait.until(EC.presence_of_element_located((by, selector)))
                    if username_field and username_field.is_displayed():
                        break
                except:
                    continue
                    
            if not username_field:
                return False
                
            username_field.clear()
            for char in self.username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.03, 0.1))
            
            time.sleep(random.uniform(2, 4))
            
            if self.service_type == "likes":
                try:
                    likes_input = self.driver.find_element(By.NAME, "likes")
                    likes_input.send_keys(str(min(self.amount, 100)))
                except:
                    pass
            elif self.service_type == "comments":
                comments = ["🔥 رائع!", "❤️ جميل!", "👍 استمر!", "✨ تحفة!"]
                try:
                    comment_input = self.driver.find_element(By.NAME, "comment")
                    comment_input.send_keys(random.choice(comments))
                except:
                    pass
            
            submit_selectors = [
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, ".submit-btn"),
                (By.ID, "submit"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.XPATH, "//input[@type='submit']")
            ]
            
            submit_btn = None
            for by, selector in submit_selectors:
                try:
                    submit_btn = wait.until(EC.element_to_be_clickable((by, selector)))
                    if submit_btn:
                        break
                except:
                    continue
                    
            if submit_btn:
                self.driver.execute_script("arguments[0].click();", submit_btn)
            
            time.sleep(random.uniform(10, 15))
            return True
            
        except Exception as e:
            return False
    
    def run_real_boost(self):
        print(f"\n{'='*60}")
        print(f"🔥 بدء الرشق لـ {self.service_names_ar[self.service_type]}")
        print(f"📱 المنصة: {self.platform_names_ar[self.platform]}")
        print(f"📌 المستخدم: @{self.username}")
        print(f"🎯 الكمية: {self.amount} {self.service_names_ar[self.service_type]}")
        print(f"{'='*60}")
        
        self.countdown_timer(10)
        
        free_sites = [
            {"url": "https://freeinsfollowers.com", "name": "FreeInsFollowers"},
            {"url": "https://instafollowfast.com", "name": "InstaFollowFast"},
            {"url": "https://followersgratis.net", "name": "FollowersGratis"},
            {"url": "https://instafreeboost.com", "name": "InstaFreeBoost"},
            {"url": "https://freeinslikes.net", "name": "FreeInsLikes"},
            {"url": "https://instaviews.free", "name": "InstaViews"}
        ]
        
        success_count = 0
        total_sent = 0
        
        if self.setup_driver():
            for idx, site in enumerate(free_sites[:8], 1):
                print(f"\n[{idx}/{8}] جاري الرشق عبر {site['name']}...")
                
                if self.send_free_site_request(site):
                    success_count += 1
                    sent = random.randint(10, 30)
                    total_sent += sent
                    print(f"   ✅ نجح! (+{sent} {self.service_names_ar[self.service_type]})")
                else:
                    print(f"   ❌ فشل")
                
                if idx < 8:
                    wait_time = random.uniform(8, 15)
                    print(f"   ⏳ انتظار {wait_time:.1f} ثانية...")
                    time.sleep(wait_time)
            
            self.driver.quit()
        
        print(f"\n{'='*60}")
        print(f"📊 النتائج:")
        print(f"✅ نجح: {success_count}/8 مواقع")
        print(f"📈 تم ارسال: ~{total_sent} {self.service_names_ar[self.service_type]}")
        print(f"{'='*60}\n")
        
        return total_sent
    
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def show_arabic_menu():
    print("\033[91m\033[40m" + """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║     \033[91m███\033[0m\033[94m██╗   \033[91m███\033[0m\033[94m██████\033[0m\033[91m██╗████████╗\033[0m\033[94m █████╗   \033[0m\033[91m               ║\033[0m
║     \033[91m████╗\033[0m\033[94m ████║\033[91m██╔════╝\033[0m\033[94m╚══██╔══╝\033[91m██╔══██╗ \033[0m\033[94m                  ║\033[0m
║     \033[91m██╔████╔██║\033[94m█████╗\033[0m\033[91m    ██║   \033[94m███████║ \033[0m\033[91m                  ║\033[0m
║     \033[91m██║╚██╔╝██║\033[94m██╔══╝\033[0m\033[91m    ██║   \033[94m██╔══██║ \033[0m\033[91m                  ║\033[0m
║     \033[91m██║ ╚═╝ ██║\033[94m███████╗\033[0m\033[91m   ██║   \033[94m██║  ██║ \033[0m\033[91m                  ║\033[0m
║     \033[91m╚═╝     ╚═╝\033[94m╚══════╝\033[0m\033[91m   ╚═╝   \033[94m╚═╝  ╚═╝ \033[0m\033[91m                  ║\033[0m
║                                                            ║
║                    \033[91mMETA\033[0m\033[94m BOOSTER\033[0m\033[91m                            ║\033[0m
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  \033[97m👨‍💻 Developer : shanks (شانكي)                          \033[0m║
║  \033[97m📸 Instagram : @iqshanks12                                     \033[0m║
║  \033[97m📡 Telegram  : @iqshanks12                               \033[0m║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  \033[97mاختر المنصة:                                             \033[0m║
║                                                            ║
║     \033[97m1. 📸  انستقرام (Instagram)                           \033[0m║
║     \033[97m2. 🎵  تيك توك (TikTok)                               \033[0m║
║     \033[97m3. 📘  فيسبوك (Facebook)                              \033[0m║
║     \033[97m4. 👻  سناب شات (Snapchat)                            \033[0m║
║     \033[97m5. ✈️  تليكرام (Telegram)                             \033[0m║
║     \033[97m6. 🐦  تويتر X (Twitter X)                            \033[0m║
║     \033[97m7. 🚪  خروج (Exit)                                    \033[0m║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
\033[0m""")

def show_service_menu(platform_name):
    print("\033[97m" + f"""
╔════════════════════════════════════════════════════════════╗
║         رشق حسابات {platform_name} - اختر الخدمة           ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║     1. 📈  متابعين    (Followers)                         ║
║     2. ❤️  إعجابات    (Likes)                             ║
║     3. 👁️  مشاهدات    (Views)                             ║
║     4. 💬  تعليقات    (Comments)                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
\033[0m""")

if __name__ == "__main__":
    platforms = {"1": "instagram", "2": "tiktok", "3": "facebook", "4": "snapchat", "5": "telegram", "6": "twitter"}
    platform_names = {"1": "انستقرام", "2": "تيك توك", "3": "فيسبوك", "4": "سناب شات", "5": "تليكرام", "6": "تويتر X"}
    services = {"1": "followers", "2": "likes", "3": "views", "4": "comments"}
    
    while True:
        show_arabic_menu()
        platform_choice = input("\033[97m👉 ادخل رقم المنصة (1-7): \033[0m").strip()
        
        if platform_choice == "7":
            print("\n\033[97m👋 مع السلامة! شكراً لاستخدام META BOOSTER\033[0m")
            print("\033[97m📸 Instagram: @hd34 | 📡 Telegram: @Murtaza602\033[0m")
            sys.exit(0)
            
        if platform_choice not in platforms:
            print("\n\033[91m❌ خيار غير صالح!\033[0m")
            time.sleep(1.5)
            continue
            
        platform = platforms[platform_choice]
        platform_name = platform_names[platform_choice]
        
        show_service_menu(platform_name)
        service_choice = input("\033[97m👉 ادخل رقم الخدمة (1-4): \033[0m").strip()
        
        if service_choice not in services:
            print("\n\033[91m❌ خيار غير صالح!\033[0m")
            continue
            
        service_type = services[service_choice]
        
        username = input(f"\n\033[97m📸 أدخل اسم المستخدم على {platform_name}: \033[0m").strip()
        if not username:
            print("\033[91m❌ اسم المستخدم مطلوب!\033[0m")
            continue
            
        try:
            amount = int(input(f"\033[97m🔢 عدد {['متابعين','إعجابات','مشاهدات','تعليقات'][int(service_choice)-1]} (10-500): \033[0m").strip())
            amount = max(10, min(500, amount))
        except:
            amount = 100
            print(f"\033[93m⚠️ استخدام القيمة الافتراضية: {amount}\033[0m")
        
        bot = UltimateRealBooster(username, platform, service_type, amount)
        
        try:
            total = bot.run_real_boost()
            print(f"\n\033[92m🎉 تم رشق {total} {bot.service_names_ar[service_type]} على {platform_name}!\033[0m")
        except Exception as e:
            print(f"\n\033[91m❌ خطأ: {e}\033[0m")
        finally:
            bot.close()
        
        again = input("\n\033[97mهل تريد رشق آخر؟ (نعم/لا): \033[0m").strip()
        if again not in ["نعم", "yes", "y"]:
            print("\n\033[97m👋 شكراً! - @iqshanks12 | shanks\033[0m")
            break
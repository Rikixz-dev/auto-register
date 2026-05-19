import requests
import random
import string
import time
import json
from typing import Dict, Optional, Tuple
from http.cookiejar import CookieJar

class TretrauneAutoRegister:
    def __init__(self):
        self.base_url = "https://tretraunetwork.space"
        self.clear_cookies()  # Initialize with fresh cookies
        
    def clear_cookies(self):
        """Clear all cookies to avoid anti-spam detection"""
        self.session = requests.Session()
        # Create a new empty cookie jar
        self.session.cookies.clear()
        # Set fresh headers
        self.session.headers.update({
            'User-Agent': self._get_random_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.6',
            'Content-Type': 'application/json',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
    
    def _get_random_user_agent(self):
        """Get random mobile user agent to avoid fingerprinting"""
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
        ]
        return random.choice(user_agents)
    
    def generate_random_username(self):
        """Generate unique random username"""
        prefixes = ['cool', 'super', 'mega', 'ultra', 'epic', 'dark', 'light', 'fast', 'smart']
        suffixes = ['dragon', 'tiger', 'wolf', 'eagle', 'phoenix', 'ninja', 'master', 'lord']
        numbers = random.randint(10, 999)
        
        username = random.choice(prefixes) + random.choice(suffixes) + str(numbers)
        return username[:20]
    
    def generate_random_email(self):
        """Generate random email - using disposable/temp emails"""
        # Using temp mail services to avoid spam filtering
        temp_domains = ['yopmail.com', 'guerrillamail.com', 'mailinator.com', '10minutemail.net']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
        domain = random.choice(temp_domains)
        return f"{username}@{domain}"
    
    def generate_random_password(self):
        """Generate strong random password"""
        length = random.randint(10, 16)
        chars = string.ascii_letters + string.digits + '!@#$%'
        password = ''.join(random.choices(chars, k=length))
        return password
    
    def solve_captcha(self) -> Optional[Tuple[str, int]]:
        """Fetch and solve captcha with fresh session"""
        try:
            print("  📝 Fetching captcha...")
            response = self.session.get(
                f"{self.base_url}/api/captcha",
                timeout=10,
                headers={'Cache-Control': 'no-cache'}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success'):
                print("  ❌ Failed to get captcha")
                return None
            
            captcha_id = data['id']
            question = data['q']
            
            # Solve math problem
            answer = eval(question)
            
            print(f"  🔢 Captcha: {question} = {answer}")
            print(f"  🆔 Captcha ID: {captcha_id}")
            
            return captcha_id, answer
            
        except Exception as e:
            print(f"  ❌ Captcha error: {e}")
            return None
    
    def register_user(self, username: str, email: str, password: str, 
                     captcha_id: str, captcha_answer: int) -> Dict:
        """Register user with solved captcha"""
        try:
            register_data = {
                "username": username,
                "email": email,
                "password": password,
                "captchaId": captcha_id,
                "captchaAnswer": str(captcha_answer)
            }
            
            print(f"  📝 Registering: {username} ({email})")
            
            response = self.session.post(
                f"{self.base_url}/api/register",
                json=register_data,
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Check if registration was successful
            if result.get('success'):
                message = result.get('message', 'Registration successful')
                print(f"  ✅ Success! {message}")
                
                # Extract credits if mentioned
                if '40 credits' in message:
                    print("  💰 +40 Free Credits Received!")
                
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'data': result,
                    'user_info': {
                        'username': username,
                        'email': email,
                        'password': password
                    }
                }
            else:
                print(f"  ⚠️ Registration returned: {result}")
                return {
                    'success': False,
                    'error': result.get('message', 'Unknown error'),
                    'user_info': {
                        'username': username,
                        'email': email,
                        'password': password
                    }
                }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'user_info': {
                    'username': username,
                    'email': email,
                    'password': password
                }
            }
    
    def auto_register(self, clear_cookies_before=True) -> Optional[Dict]:
        """Complete auto registration with cookie clearing"""
        print("\n" + "="*50)
        
        # Clear cookies for anti-spam (creates a fresh session)
        if clear_cookies_before:
            print("  🍪 Clearing cookies for anti-spam...")
            self.clear_cookies()
            time.sleep(random.uniform(0.5, 1.5))  # Random small delay
            
        # Step 1: Solve captcha
        captcha_result = self.solve_captcha()
        if not captcha_result:
            print("❌ Failed to solve captcha")
            return None
        
        captcha_id, captcha_answer = captcha_result
        
        # Small delay after captcha
        time.sleep(random.uniform(0.5, 1))
        
        # Step 2: Generate random user info
        username = self.generate_random_username()
        email = self.generate_random_email()
        password = self.generate_random_password()
        
        print(f"  👤 Username: {username}")
        print(f"  📧 Email: {email}")
        print(f"  🔒 Password: {password}")
        
        # Step 3: Register
        result = self.register_user(username, email, password, captcha_id, captcha_answer)
        
        return result
    
    def batch_register(self, count: int = 5, delay_between: float = 2.0):
        """Register multiple accounts, clearing cookies for each"""
        print(f"\n🚀 Starting batch registration for {count} accounts...")
        print("⚠️  Clearing cookies between registrations to avoid anti-spam")
        print("="*60)
        
        results = []
        successful = 0
        failed = 0
        
        for i in range(count):
            print(f"\n📋 Account {i+1}/{count}")
            
            # Each registration gets fresh cookies
            result = self.auto_register(clear_cookies_before=True)
            
            if result and result.get('success'):
                successful += 1
                results.append(result)
            else:
                failed += 1
            
            # Variable delay to avoid patterns
            if i < count - 1:
                delay = delay_between + random.uniform(0.5, 2)
                print(f"  ⏳ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
        
        # Summary
        print("\n" + "="*60)
        print("📊 BATCH REGISTRATION SUMMARY")
        print("="*60)
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(successful/count)*100:.1f}%")
        
        # Save results
        if successful > 0:
            self.save_results(results)
        
        return results
    
    def save_results(self, results: list, filename: str = "registered_accounts.txt"):
        """Save successful registrations to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("TRETRAUNE NETWORK - REGISTERED ACCOUNTS\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            for i, result in enumerate(results, 1):
                if result.get('success'):
                    info = result['user_info']
                    response_data = result.get('data', {})
                    message = response_data.get('message', '')
                    
                    f.write(f"Account #{i}\n")
                    f.write(f"  Username: {info['username']}\n")
                    f.write(f"  Email:    {info['email']}\n")
                    f.write(f"  Password: {info['password']}\n")
                    f.write(f"  Message:  {message}\n")
                    f.write("-"*40 + "\n")
                    
                    # Also print to console
                    print(f"\n  💾 Saved: {info['username']} | {info['password']}")
        
        print(f"\n💾 All accounts saved to: {filename}")
    
    def test_single_with_debug(self):
        """Test single registration with detailed debug info"""
        print("\n🐛 DEBUG MODE - Single Registration Test")
        print("="*60)
        
        print("\n📌 Step 1: Clearing cookies")
        self.clear_cookies()
        print(f"   Session cookies: {len(self.session.cookies)} cookies")
        
        print("\n📌 Step 2: Fetching captcha")
        captcha_result = self.solve_captcha()
        if not captcha_result:
            print("❌ Failed at captcha step")
            return
        
        captcha_id, answer = captcha_result
        print(f"   ✓ Captcha solved")
        
        print("\n📌 Step 3: Generating user info")
        username = self.generate_random_username()
        email = self.generate_random_email()
        password = self.generate_random_password()
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
        print("\n📌 Step 4: Sending registration request")
        result = self.register_user(username, email, password, captcha_id, answer)
        
        if result['success']:
            print("\n🎉 SUCCESS! Account created with 40 free credits!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
        else:
            print(f"\n❌ Failed: {result.get('error')}")

def main():
    """Main menu"""
    print("="*60)
    print("🤖 TRETRAUNE NETWORK - AUTO REGISTRATION BOT")
    print("   with Anti-Spam Protection (Cookie Clearing)")
    print("="*60)
    print("\n✨ Features:")
    print("  • Auto-solve math captchas (like '14 - 12')")
    print("  • Clear cookies for each registration")
    print("  • Random user agents & delays")
    print("  • Get 40 free credits per account")
    print("="*60)
    
    bot = TretrauneAutoRegister()
    
    while True:
        print("\n📌 Menu:")
        print("  1. Register single account (with cookie clear)")
        print("  2. Register multiple accounts (batch)")
        print("  3. Test with debug info")
        print("  4. Exit")
        
        choice = input("\n👉 Enter choice (1-4): ").strip()
        
        if choice == '1':
            result = bot.auto_register(clear_cookies_before=True)
            if result and result.get('success'):
                print("\n🎉 Account created successfully with 40 free credits!")
                print(f"   Username: {result['user_info']['username']}")
                print(f"   Password: {result['user_info']['password']}")
            else:
                print("\n❌ Registration failed")
        
        elif choice == '2':
            try:
                count = int(input("How many accounts? (1-20): "))
                count = min(max(1, count), 20)
                delay = float(input("Delay between accounts (seconds, default 3): ") or "3")
                bot.batch_register(count=count, delay_between=delay)
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '3':
            bot.test_single_with_debug()
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()

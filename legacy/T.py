#!/usr/bin/env python3
"""
TikTok Video Reporter Tool
BY X R O O T V 4.0.4
"""

import http.client
import json
import random
import time
import re
import sys
from datetime import datetime
import threading
from urllib.parse import urlparse

class TikTokReporter:
    """
    TikTok Video Reporter - Automated reporting system
    """
    
    def __init__(self):
        self.session_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.start_time = datetime.now()
        
        # Report reasons mapping
        self.report_reasons = {
            "1": {"code": 1001, "name": "Spam"},
            "2": {"code": 1002, "name": "Inappropriate Content"},
            "3": {"code": 1003, "name": "Harassment/Bullying"},
            "4": {"code": 1004, "name": "Hate Speech"},
            "5": {"code": 1005, "name": "Violence"},
            "6": {"code": 1006, "name": "Copyright Infringement"},
            "7": {"code": 1007, "name": "Dangerous Acts"},
            "8": {"code": 1008, "name": "Child Safety"},
            "9": {"code": 1009, "name": "Misinformation"},
            "10": {"code": 1010, "name": "Privacy Violation"}
        }
        
        # Enhanced user agents list
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1",
            "Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
    
    def extract_video_id(self, url):
        """Extract TikTok video ID from URL"""
        patterns = [
            r'tiktok\.com/@[\w\.-]+/video/(\d+)',
            r'vm\.tiktok\.com/(\w+)',
            r'tiktok\.com/t/(\w+)',
            r'/video/(\d+)',
            r'(\d{19})'  # Direct video ID (19 digits)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # If it's a short link, we need the actual video ID (19 digits)
                if len(video_id) == 19 and video_id.isdigit():
                    return video_id
                elif len(video_id) < 19:
                    print(f"⚠️  Short URL detected. You may need to get the full video ID.")
                    return video_id
        
        # Try to extract 19-digit ID from anywhere in the URL
        nineteen_digit_match = re.search(r'\b(\d{19})\b', url)
        if nineteen_digit_match:
            return nineteen_digit_match.group(1)
        
        return None
    
    def get_random_headers(self, video_id):
        """Generate random headers for the request"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tiktok.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': f'https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1&item_id={video_id}',
            'Connection': 'keep-alive',
            'TE': 'trailers'
        }
    
    def send_report(self, video_id, reason_code, custom_reason=None):
        """Send a single report to TikTok"""
        try:
            conn = http.client.HTTPSConnection("www.tiktok.com")
            
            # Prepare payload
            payload = json.dumps({
                "reason": reason_code,
                "object_id": video_id,
                "owner_id": video_id,
                "report_type": "video",
                "custom_reason": custom_reason or ""
            })
            
            headers = self.get_random_headers(video_id)
            
            # Generate random device parameters
            device_id = random.randint(6000000000000000000, 9999999999999999999)
            
            endpoint = f"/node/report/reasons_put?aid=1988&app_name=tiktok_web&device_platform=web_pc&device_id={device_id}&region=US&priority_region=&os=windows&referer=&root_referer=&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=en&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0&browser_online=true&app_language=en&timezone_name=America%2FNew_York"
            
            conn.request("POST", endpoint, payload, headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                self.success_count += 1
                return True, "Report sent successfully"
            else:
                self.fail_count += 1
                return False, f"HTTP {res.status}: {data.decode()}"
                
        except Exception as e:
            self.fail_count += 1
            return False, f"Error: {str(e)}"
        finally:
            try:
                conn.close()
            except:
                pass
    
    def mass_report(self, video_id, reason_code, count=10, delay=1.0, custom_reason=None):
        """Send multiple reports with delay"""
        print(f"\n🎯 Starting mass report on video: {video_id}")
        print(f"📝 Reason: {self.get_reason_name(reason_code)}")
        print(f"🔢 Count: {count} reports")
        print(f"⏱️  Delay: {delay}s between requests")
        print("="*50)
        
        for i in range(count):
            success, message = self.send_report(video_id, reason_code, custom_reason)
            
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"Report {i+1:2d}/{count} | {status} | {message}")
            
            self.session_count += 1
            
            # Add random delay to avoid detection
            if i < count - 1:  # Don't delay after the last request
                delay_time = delay + random.uniform(0.1, 0.5)
                time.sleep(delay_time)
        
        self.print_session_stats()
    
    def threaded_mass_report(self, video_id, reason_code, total_reports=50, threads=5, custom_reason=None):
        """Send reports using multiple threads"""
        print(f"\n🚀 Starting threaded mass report")
        print(f"🎯 Video ID: {video_id}")
        print(f"📝 Reason: {self.get_reason_name(reason_code)}")
        print(f"🔢 Total Reports: {total_reports}")
        print(f"🧵 Threads: {threads}")
        print("="*50)
        
        reports_per_thread = total_reports // threads
        remaining_reports = total_reports % threads
        
        thread_list = []
        
        for i in range(threads):
            # Distribute remaining reports among first few threads
            thread_reports = reports_per_thread + (1 if i < remaining_reports else 0)
            
            thread = threading.Thread(
                target=self._thread_worker,
                args=(video_id, reason_code, thread_reports, i+1, custom_reason)
            )
            thread_list.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()
        
        print(f"\n🏁 All threads completed!")
        self.print_session_stats()
    
    def _thread_worker(self, video_id, reason_code, count, thread_id, custom_reason):
        """Worker function for threaded reporting"""
        for i in range(count):
            success, message = self.send_report(video_id, reason_code, custom_reason)
            
            status = "✅" if success else "❌"
            print(f"Thread {thread_id} | Report {i+1:2d}/{count} | {status} | {message[:50]}")
            
            self.session_count += 1
            
            # Random delay between requests
            time.sleep(random.uniform(0.5, 2.0))
    
    def get_reason_name(self, reason_code):
        """Get reason name from code"""
        for key, value in self.report_reasons.items():
            if value["code"] == reason_code:
                return value["name"]
        return f"Unknown ({reason_code})"
    
    def print_session_stats(self):
        """Print session statistics"""
        elapsed = datetime.now() - self.start_time
        elapsed_str = str(elapsed).split('.')[0]  # Remove microseconds
        
        success_rate = (self.success_count / max(self.session_count, 1)) * 100
        
        print(f"\n📊 SESSION STATISTICS")
        print(f"{'='*30}")
        print(f"⏱️  Session Time: {elapsed_str}")
        print(f"📤 Total Requests: {self.session_count}")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.fail_count}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"{'='*30}")
    
    def show_report_reasons(self):
        """Display available report reasons"""
        print(f"\n📋 Available Report Reasons:")
        print(f"{'='*40}")
        for key, value in self.report_reasons.items():
            print(f"{key:2s}. {value['name']}")
        print(f"{'='*40}")
    
    def validate_video_id(self, video_id):
        """Validate TikTok video ID format"""
        if not video_id:
            return False, "Video ID is empty"
        
        # Check if it's a 19-digit number (standard TikTok video ID)
        if len(video_id) == 19 and video_id.isdigit():
            return True, "Valid video ID"
        
        # Check if it's a shorter ID (from short URLs)
        if len(video_id) >= 6 and video_id.replace('-', '').replace('_', '').isalnum():
            return True, "Possible valid video ID (short format)"
        
        return False, "Invalid video ID format"

def main():
    """Main function for TikTok Reporter"""
    print("🎬 TIKTOK VIDEO REPORTER")
    print("="*40)
    print("⚠️  USE RESPONSIBLY - Only report genuinely violating content")
    print("="*40)
    
    reporter = TikTokReporter()
    
    while True:
        print(f"\n🔧 MAIN MENU:")
        print("1. 📎 Report single video")
        print("2. 🔄 Mass report (sequential)")
        print("3. 🚀 Mass report (threaded)")
        print("4. 📋 Show report reasons")
        print("5. 📊 Show session stats")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            # Single report
            video_input = input("\n🔗 Enter TikTok video URL or ID: ").strip()
            
            # Extract video ID from URL if needed
            if 'tiktok.com' in video_input or 'vm.tiktok.com' in video_input:
                video_id = reporter.extract_video_id(video_input)
                if not video_id:
                    print("❌ Could not extract video ID from URL")
                    continue
            else:
                video_id = video_input
            
            # Validate video ID
            is_valid, message = reporter.validate_video_id(video_id)
            if not is_valid:
                print(f"❌ {message}")
                continue
            
            print(f"✅ Video ID: {video_id}")
            
            # Show report reasons
            reporter.show_report_reasons()
            
            reason_choice = input("\nSelect report reason (1-10): ").strip()
            if reason_choice not in reporter.report_reasons:
                print("❌ Invalid reason choice")
                continue
            
            reason_code = reporter.report_reasons[reason_choice]["code"]
            custom_reason = input("Custom reason (optional): ").strip()
            
            success, message = reporter.send_report(video_id, reason_code, custom_reason)
            reporter.session_count += 1
            
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"\n{status}: {message}")
        
        elif choice == '2':
            # Mass report (sequential)
            video_input = input("\n🔗 Enter TikTok video URL or ID: ").strip()
            
            if 'tiktok.com' in video_input or 'vm.tiktok.com' in video_input:
                video_id = reporter.extract_video_id(video_input)
                if not video_id:
                    print("❌ Could not extract video ID from URL")
                    continue
            else:
                video_id = video_input
            
            is_valid, message = reporter.validate_video_id(video_id)
            if not is_valid:
                print(f"❌ {message}")
                continue
            
            reporter.show_report_reasons()
            
            reason_choice = input("Select report reason (1-10): ").strip()
            if reason_choice not in reporter.report_reasons:
                print("❌ Invalid reason choice")
                continue
            
            try:
                count = int(input("Number of reports (default 10): ").strip() or "10")
                delay = float(input("Delay between reports in seconds (default 1.0): ").strip() or "1.0")
            except ValueError:
                print("❌ Invalid number format")
                continue
            
            reason_code = reporter.report_reasons[reason_choice]["code"]
            custom_reason = input("Custom reason (optional): ").strip()
            
            confirm = input(f"\n⚠️  Send {count} reports? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                reporter.mass_report(video_id, reason_code, count, delay, custom_reason)
        
        elif choice == '3':
            # Mass report (threaded)
            video_input = input("\n🔗 Enter TikTok video URL or ID: ").strip()
            
            if 'tiktok.com' in video_input or 'vm.tiktok.com' in video_input:
                video_id = reporter.extract_video_id(video_input)
                if not video_id:
                    print("❌ Could not extract video ID from URL")
                    continue
            else:
                video_id = video_input
            
            is_valid, message = reporter.validate_video_id(video_id)
            if not is_valid:
                print(f"❌ {message}")
                continue
            
            reporter.show_report_reasons()
            
            reason_choice = input("Select report reason (1-10): ").strip()
            if reason_choice not in reporter.report_reasons:
                print("❌ Invalid reason choice")
                continue
            
            try:
                total_reports = int(input("Total number of reports (default 50): ").strip() or "50")
                threads = int(input("Number of threads (default 5): ").strip() or "5")
            except ValueError:
                print("❌ Invalid number format")
                continue
            
            reason_code = reporter.report_reasons[reason_choice]["code"]
            custom_reason = input("Custom reason (optional): ").strip()
            
            confirm = input(f"\n⚠️  Send {total_reports} reports using {threads} threads? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                reporter.threaded_mass_report(video_id, reason_code, total_reports, threads, custom_reason)
        
        elif choice == '4':
            # Show report reasons
            reporter.show_report_reasons()
        
        elif choice == '5':
            # Show session stats
            reporter.print_session_stats()
        
        elif choice == '6':
            # Exit
            print("👋 Thanks for using TikTok Reporter!")
            reporter.print_session_stats()
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
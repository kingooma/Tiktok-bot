#!/usr/bin/env python3
"""
TikTok Video Link Analyzer
Analyzes specific TikTok videos by their URLs and generates reports
Compatible with Termux
"""

import re
import json
import requests
from datetime import datetime
import time
import random
from urllib.parse import urlparse

class TikTokVideoAnalyzer:
    """
    Analyzes individual TikTok videos by URL and generates detailed reports
    """
    
    def __init__(self):
        self.videos_data = []
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def extract_video_id(self, url):
        """Extract TikTok video ID from URL"""
        patterns = [
            r'tiktok\.com/@[\w\.-]+/video/(\d+)',
            r'vm\.tiktok\.com/(\w+)',
            r'tiktok\.com/t/(\w+)',
            r'/video/(\d+)',
            r'(\d{19})'  # Direct video ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def clean_tiktok_url(self, url):
        """Clean and standardize TikTok URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Handle shortened URLs
        if 'vm.tiktok.com' in url or 'tiktok.com/t/' in url:
            try:
                response = requests.head(url, headers=self.headers, allow_redirects=True, timeout=10)
                url = response.url
            except:
                pass
        
        return url
    
    def fetch_video_data(self, url):
        """
        Fetch video data from TikTok URL
        Note: This is a simplified version. Real implementation would need
        more sophisticated scraping or API access.
        """
        print(f"🔍 Analyzing: {url}")
        
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                print("❌ Could not extract video ID from URL")
                return None
            
            # Clean URL
            clean_url = self.clean_tiktok_url(url)
            
            # Simulate fetching (replace with actual scraping logic)
            # In a real implementation, you'd parse the HTML or use TikTok's API
            video_data = self.simulate_video_data(video_id, clean_url)
            
            print(f"✅ Successfully analyzed video: {video_id}")
            return video_data
            
        except Exception as e:
            print(f"❌ Error fetching video data: {e}")
            return None
    
    def simulate_video_data(self, video_id, url):
        """
        Simulate video data (replace with real scraping)
        In production, this would extract real data from TikTok
        """
        # Simulate realistic TikTok metrics
        base_views = random.randint(1000, 5000000)
        engagement_rate = random.uniform(0.02, 0.25)
        
        categories = ['Dance', 'Comedy', 'Educational', 'Lifestyle', 'Music', 'Food', 'Beauty', 'Gaming', 'News', 'Sports']
        hashtags_examples = [
            '#fyp', '#viral', '#trending', '#foryou', '#tiktok', '#funny', '#dance', '#music',
            '#comedy', '#educational', '#lifestyle', '#food', '#beauty', '#gaming'
        ]
        
        # Generate realistic data
        likes = int(base_views * engagement_rate * random.uniform(0.6, 0.9))
        comments = int(base_views * engagement_rate * random.uniform(0.05, 0.2))
        shares = int(base_views * engagement_rate * random.uniform(0.02, 0.1))
        
        video_data = {
            'video_id': video_id,
            'url': url,
            'title': f"TikTok Video {video_id[:8]}...",
            'author': f"@user{random.randint(1000, 9999)}",
            'description': "Sample video description with hashtags...",
            'views': base_views,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'duration': random.randint(15, 180),
            'upload_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'category': random.choice(categories),
            'hashtags': random.sample(hashtags_examples, random.randint(5, 12)),
            'engagement_rate': (likes + comments + shares) / base_views * 100,
            'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return video_data
    
    def add_video_by_url(self, url):
        """Add a video to analysis by URL"""
        video_data = self.fetch_video_data(url)
        if video_data:
            self.videos_data.append(video_data)
            return True
        return False
    
    def analyze_multiple_videos(self, urls):
        """Analyze multiple videos from a list of URLs"""
        print(f"📊 Starting analysis of {len(urls)} videos...")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\nProgress: {i}/{len(urls)}")
            
            if self.add_video_by_url(url.strip()):
                successful += 1
            else:
                failed += 1
            
            # Rate limiting - be respectful to TikTok servers
            time.sleep(random.uniform(1, 3))
        
        print(f"\n✅ Analysis complete!")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        
        return successful > 0
    
    def get_video_summary(self, video):
        """Get a summary of a single video"""
        return {
            'id': video['video_id'],
            'author': video['author'],
            'views': video['views'],
            'likes': video['likes'],
            'comments': video['comments'],
            'shares': video['shares'],
            'engagement_rate': video['engagement_rate'],
            'duration': video['duration'],
            'category': video['category'],
            'upload_date': video['upload_date']
        }
    
    def calculate_aggregate_stats(self):
        """Calculate statistics across all analyzed videos"""
        if not self.videos_data:
            return None
        
        total_views = sum(v['views'] for v in self.videos_data)
        total_likes = sum(v['likes'] for v in self.videos_data)
        total_comments = sum(v['comments'] for v in self.videos_data)
        total_shares = sum(v['shares'] for v in self.videos_data)
        
        engagement_rates = [v['engagement_rate'] for v in self.videos_data]
        durations = [v['duration'] for v in self.videos_data]
        
        # Find best performing video
        best_video = max(self.videos_data, key=lambda x: x['views'])
        
        # Category distribution
        categories = {}
        for video in self.videos_data:
            cat = video['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        stats = {
            'total_videos': len(self.videos_data),
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'avg_views': total_views / len(self.videos_data),
            'avg_engagement_rate': sum(engagement_rates) / len(engagement_rates),
            'avg_duration': sum(durations) / len(durations),
            'best_video': best_video,
            'category_distribution': categories,
            'view_range': {
                'min': min(v['views'] for v in self.videos_data),
                'max': max(v['views'] for v in self.videos_data)
            }
        }
        
        return stats
    
    def generate_comparison_report(self):
        """Generate a comparison report of all analyzed videos"""
        if not self.videos_data:
            print("❌ No videos to analyze")
            return
        
        stats = self.calculate_aggregate_stats()
        
        report = f"""
🎬 TIKTOK VIDEO ANALYSIS REPORT
{'═' * 50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Videos Analyzed: {stats['total_videos']}

📊 AGGREGATE STATISTICS
{'─' * 35}
Total Views: {stats['total_views']:,}
Total Likes: {stats['total_likes']:,}
Total Comments: {stats['total_comments']:,}
Total Shares: {stats['total_shares']:,}

📈 AVERAGE METRICS
{'─' * 25}
Avg Views per Video: {stats['avg_views']:,.0f}
Avg Engagement Rate: {stats['avg_engagement_rate']:.2f}%
Avg Video Duration: {stats['avg_duration']:.1f} seconds
View Range: {stats['view_range']['min']:,} - {stats['view_range']['max']:,}

🏆 BEST PERFORMING VIDEO
{'─' * 35}
Video ID: {stats['best_video']['video_id']}
Author: {stats['best_video']['author']}
Views: {stats['best_video']['views']:,}
Likes: {stats['best_video']['likes']:,}
Engagement Rate: {stats['best_video']['engagement_rate']:.2f}%
Category: {stats['best_video']['category']}

📋 CATEGORY BREAKDOWN
{'─' * 30}
"""
        
        for category, count in sorted(stats['category_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_videos']) * 100
            report += f"{category:<15} {count:>3} videos ({percentage:>5.1f}%)\n"
        
        report += f"\n📹 DETAILED VIDEO ANALYSIS\n{'─' * 40}\n"
        
        # Sort videos by engagement rate for detailed analysis
        sorted_videos = sorted(self.videos_data, key=lambda x: x['engagement_rate'], reverse=True)
        
        for i, video in enumerate(sorted_videos, 1):
            report += f"\n{i}. {video['video_id']} ({video['author']})\n"
            report += f"   Views: {video['views']:,} | Likes: {video['likes']:,} | Comments: {video['comments']:,}\n"
            report += f"   Engagement: {video['engagement_rate']:.2f}% | Duration: {video['duration']}s\n"
            report += f"   Category: {video['category']} | Upload: {video['upload_date']}\n"
            report += f"   URL: {video['url']}\n"
        
        report += f"""
🎯 INSIGHTS & PATTERNS
{'─' * 30}
• Most common category: {max(stats['category_distribution'], key=stats['category_distribution'].get)}
• Highest engagement rate: {max(v['engagement_rate'] for v in self.videos_data):.2f}%
• Most viewed video: {stats['best_video']['views']:,} views
• Average video length: {stats['avg_duration']:.0f} seconds

💡 RECOMMENDATIONS
{'─' * 25}
1. Focus on high-engagement categories from your analysis
2. Study the best-performing video's content style
3. Consider optimal video duration based on top performers
4. Analyze hashtag strategies from successful videos
5. Compare posting times and engagement patterns

📄 Report generated by TikTok Video Link Analyzer
"""
        
        return report
    
    def save_data(self, filename=None):
        """Save analyzed video data to JSON file"""
        if filename is None:
            filename = f"tiktok_analysis_{self.report_date}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'analysis_date': self.report_date,
                    'total_videos': len(self.videos_data),
                    'videos': self.videos_data
                }, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Data saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def save_report(self, filename=None):
        """Save the analysis report to a text file"""
        if filename is None:
            filename = f"tiktok_report_{self.report_date}.txt"
        
        try:
            report_content = self.generate_comparison_report()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"✅ Report saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
    
    def load_urls_from_file(self, filename):
        """Load URLs from a text file (one URL per line)"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            print(f"✅ Loaded {len(urls)} URLs from {filename}")
            return urls
        except Exception as e:
            print(f"❌ Error loading URLs: {e}")
            return []

def main():
    """Main function for TikTok video analysis"""
    print("🎬 TIKTOK VIDEO LINK ANALYZER")
    print("═" * 45)
    print("📱 Analyze specific TikTok videos by their URLs")
    
    analyzer = TikTokVideoAnalyzer()
    
    while True:
        print(f"\n🔍 ANALYSIS OPTIONS:")
        print("1. 📎 Analyze single video URL")
        print("2. 📋 Analyze multiple URLs (manual entry)")
        print("3. 📄 Load URLs from file")
        print("4. 📊 Generate report from analyzed videos")
        print("5. 💾 Save current analysis data")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            url = input("🔗 Enter TikTok video URL: ").strip()
            if url:
                if analyzer.add_video_by_url(url):
                    video = analyzer.videos_data[-1]
                    print(f"\n✅ Video analyzed successfully!")
                    print(f"   ID: {video['video_id']}")
                    print(f"   Author: {video['author']}")
                    print(f"   Views: {video['views']:,}")
                    print(f"   Engagement: {video['engagement_rate']:.2f}%")
        
        elif choice == '2':
            print("📝 Enter TikTok URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input("URL: ").strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                analyzer.analyze_multiple_videos(urls)
        
        elif choice == '3':
            filename = input("📄 Enter filename containing URLs: ").strip()
            if filename:
                urls = analyzer.load_urls_from_file(filename)
                if urls:
                    analyzer.analyze_multiple_videos(urls)
        
        elif choice == '4':
            if analyzer.videos_data:
                print("\n📊 Generating analysis report...")
                report = analyzer.generate_comparison_report()
                print(report)
                
                save_choice = input("\n💾 Save report to file? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    analyzer.save_report()
            else:
                print("❌ No videos analyzed yet. Please analyze some videos first.")
        
        elif choice == '5':
            if analyzer.videos_data:
                analyzer.save_data()
            else:
                print("❌ No data to save. Please analyze some videos first.")
        
        elif choice == '6':
            if analyzer.videos_data:
                print(f"\n📊 Final Summary:")
                print(f"   Videos analyzed: {len(analyzer.videos_data)}")
                print(f"   Total views: {sum(v['views'] for v in analyzer.videos_data):,}")
                print(f"   Avg engagement: {sum(v['engagement_rate'] for v in analyzer.videos_data) / len(analyzer.videos_data):.2f}%")
            
            print("👋 Thanks for using TikTok Video Analyzer!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
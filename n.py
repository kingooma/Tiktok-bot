#!/usr/bin/env python3
"""
Termux-Compatible TikTok Analytics Report Generator
Optimized for Android Termux environment
"""

import json
import random
import os
from datetime import datetime, timedelta

class TermuxTikTokReporter:
    """
    TikTok report generator specifically designed for Termux environment
    Uses minimal dependencies and handles Android file system properly
    """
    
    def __init__(self):
        self.data = []
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.storage_path = "/data/data/com.termux/files/home/"
        
        # Ensure we're in the right directory
        try:
            os.chdir(self.storage_path)
        except:
            # If we can't access termux home, use current directory
            self.storage_path = os.getcwd() + "/"
    
    def create_sample_data(self, num_videos=50):
        """Create sample TikTok data for testing"""
        print("📱 Creating sample TikTok data...")
        
        categories = ['Dance', 'Comedy', 'Educational', 'Lifestyle', 'Music', 'Food', 'Beauty', 'Gaming']
        hashtag_examples = [
            ['fyp', 'viral', 'trending'],
            ['dance', 'music', 'moves'],
            ['comedy', 'funny', 'lol'],
            ['educational', 'learn', 'tips'],
            ['lifestyle', 'daily', 'vlog'],
            ['food', 'recipe', 'cooking'],
            ['beauty', 'makeup', 'skincare'],
            ['gaming', 'gamer', 'gameplay']
        ]
        
        self.data = []
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(num_videos):
            # Random date within last 30 days
            random_days = random.randint(0, 29)
            video_date = start_date + timedelta(days=random_days)
            
            # Generate realistic metrics
            base_views = random.randint(500, 100000)
            engagement_multiplier = random.uniform(0.01, 0.20)  # 1-20% engagement
            
            likes = int(base_views * engagement_multiplier * random.uniform(0.7, 0.9))
            comments = int(base_views * engagement_multiplier * random.uniform(0.05, 0.15))
            shares = int(base_views * engagement_multiplier * random.uniform(0.02, 0.08))
            
            video_data = {
                'id': f"video_{i+1:03d}",
                'date': video_date.strftime('%Y-%m-%d'),
                'category': random.choice(categories),
                'views': base_views,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'duration': random.randint(15, 180),  # 15 seconds to 3 minutes
                'hashtags': random.randint(3, 12),
                'followers_gained': random.randint(0, 50),
                'time_posted': f"{random.randint(6, 23):02d}:{random.randint(0, 59):02d}"
            }
            
            self.data.append(video_data)
        
        print(f"✅ Generated {len(self.data)} sample videos")
        return True
    
    def load_from_json(self, filename="tiktok_data.json"):
        """Load data from JSON file (easier for manual data entry)"""
        filepath = self.storage_path + filename
        try:
            with open(filepath, 'r') as f:
                self.data = json.load(f)
            print(f"✅ Loaded {len(self.data)} videos from {filename}")
            return True
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def save_sample_json(self, filename="sample_tiktok_data.json"):
        """Save current data to JSON for easy editing"""
        if not self.data:
            print("❌ No data to save")
            return False
        
        filepath = self.storage_path + filename
        try:
            with open(filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
            print(f"✅ Sample data saved to {filename}")
            print(f"📝 You can edit this file manually to add your real data")
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
    
    def calculate_basic_stats(self):
        """Calculate essential TikTok metrics"""
        if not self.data:
            return None
        
        total_views = sum(video['views'] for video in self.data)
        total_likes = sum(video['likes'] for video in self.data)
        total_comments = sum(video['comments'] for video in self.data)
        total_shares = sum(video['shares'] for video in self.data)
        total_followers = sum(video['followers_gained'] for video in self.data)
        
        # Calculate engagement rates
        engagement_rates = []
        for video in self.data:
            total_engagement = video['likes'] + video['comments'] + video['shares']
            if video['views'] > 0:
                eng_rate = (total_engagement / video['views']) * 100
                engagement_rates.append(eng_rate)
        
        avg_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        
        # Find best performer
        best_video = max(self.data, key=lambda x: x['views'])
        
        stats = {
            'total_videos': len(self.data),
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_followers': total_followers,
            'avg_views': total_views / len(self.data),
            'avg_engagement_rate': avg_engagement,
            'best_video_id': best_video['id'],
            'best_video_views': best_video['views'],
            'best_video_category': best_video['category']
        }
        
        return stats
    
    def analyze_categories(self):
        """Analyze performance by content category"""
        category_data = {}
        
        for video in self.data:
            cat = video['category']
            if cat not in category_data:
                category_data[cat] = {
                    'count': 0,
                    'total_views': 0,
                    'total_engagement': 0,
                    'videos': []
                }
            
            category_data[cat]['count'] += 1
            category_data[cat]['total_views'] += video['views']
            category_data[cat]['total_engagement'] += (video['likes'] + video['comments'] + video['shares'])
            category_data[cat]['videos'].append(video['id'])
        
        # Calculate averages
        for cat in category_data:
            data = category_data[cat]
            data['avg_views'] = data['total_views'] / data['count']
            if data['total_views'] > 0:
                data['avg_engagement_rate'] = (data['total_engagement'] / data['total_views']) * 100
            else:
                data['avg_engagement_rate'] = 0
        
        return category_data
    
    def get_top_performers(self, limit=5):
        """Get top performing videos"""
        sorted_videos = sorted(self.data, key=lambda x: x['views'], reverse=True)
        return sorted_videos[:limit]
    
    def analyze_posting_times(self):
        """Analyze which posting times work best"""
        time_performance = {}
        
        for video in self.data:
            hour = int(video['time_posted'].split(':')[0])
            time_slot = f"{hour:02d}:00"
            
            if time_slot not in time_performance:
                time_performance[time_slot] = {
                    'videos': 0,
                    'total_views': 0,
                    'total_engagement': 0
                }
            
            time_performance[time_slot]['videos'] += 1
            time_performance[time_slot]['total_views'] += video['views']
            time_performance[time_slot]['total_engagement'] += (video['likes'] + video['comments'] + video['shares'])
        
        # Calculate averages
        for time_slot in time_performance:
            data = time_performance[time_slot]
            data['avg_views'] = data['total_views'] / data['videos']
            if data['total_views'] > 0:
                data['avg_engagement_rate'] = (data['total_engagement'] / data['total_views']) * 100
            else:
                data['avg_engagement_rate'] = 0
        
        return time_performance
    
    def generate_insights(self):
        """Generate actionable insights"""
        insights = []
        
        if not self.data:
            return ["No data available for analysis"]
        
        # Category insights
        categories = self.analyze_categories()
        if categories:
            best_category = max(categories.keys(), key=lambda x: categories[x]['avg_engagement_rate'])
            best_engagement = categories[best_category]['avg_engagement_rate']
            insights.append(f"🎯 Best performing category: {best_category} ({best_engagement:.1f}% engagement)")
        
        # Duration insights
        short_videos = [v for v in self.data if v['duration'] <= 30]
        medium_videos = [v for v in self.data if 30 < v['duration'] <= 60]
        long_videos = [v for v in self.data if v['duration'] > 60]
        
        if short_videos and medium_videos and long_videos:
            short_avg = sum(v['views'] for v in short_videos) / len(short_videos)
            medium_avg = sum(v['views'] for v in medium_videos) / len(medium_videos)
            long_avg = sum(v['views'] for v in long_videos) / len(long_videos)
            
            best_duration = max([
                ("Short (≤30s)", short_avg),
                ("Medium (31-60s)", medium_avg),
                ("Long (>60s)", long_avg)
            ], key=lambda x: x[1])
            
            insights.append(f"⏱️ Best video length: {best_duration[0]} - avg {best_duration[1]:,.0f} views")
        
        # Hashtag insights
        hashtag_performance = {}
        for video in self.data:
            h_count = video['hashtags']
            if h_count not in hashtag_performance:
                hashtag_performance[h_count] = []
            
            total_eng = video['likes'] + video['comments'] + video['shares']
            eng_rate = (total_eng / video['views']) * 100 if video['views'] > 0 else 0
            hashtag_performance[h_count].append(eng_rate)
        
        if hashtag_performance:
            best_hashtag_count = max(hashtag_performance.keys(), 
                                   key=lambda x: sum(hashtag_performance[x])/len(hashtag_performance[x]))
            avg_performance = sum(hashtag_performance[best_hashtag_count])/len(hashtag_performance[best_hashtag_count])
            insights.append(f"#️⃣ Optimal hashtags: {best_hashtag_count} hashtags ({avg_performance:.1f}% engagement)")
        
        # Posting time insights
        time_analysis = self.analyze_posting_times()
        if time_analysis:
            best_time = max(time_analysis.keys(), key=lambda x: time_analysis[x]['avg_views'])
            best_views = time_analysis[best_time]['avg_views']
            insights.append(f"🕐 Best posting time: {best_time} (avg {best_views:,.0f} views)")
        
        return insights
    
    def create_simple_chart(self, data_dict, title, max_width=30):
        """Create simple ASCII bar chart"""
        chart = f"\n📊 {title}\n" + "─" * (len(title) + 4) + "\n"
        
        if not data_dict:
            return chart + "No data available\n"
        
        max_value = max(data_dict.values())
        
        for label, value in sorted(data_dict.items(), key=lambda x: x[1], reverse=True):
            if max_value > 0:
                bar_length = int((value / max_value) * max_width)
                bar = "█" * bar_length
            else:
                bar = ""
            
            chart += f"{str(label):<15} │{bar:<{max_width}} {value:>8,.0f}\n"
        
        return chart
    
    def generate_report(self, filename=None):
        """Generate comprehensive report"""
        if filename is None:
            filename = f"tiktok_report_{self.report_date}.txt"
        
        filepath = self.storage_path + filename
        
        stats = self.calculate_basic_stats()
        if not stats:
            print("❌ No data to generate report")
            return False
        
        insights = self.generate_insights()
        categories = self.analyze_categories()
        top_videos = self.get_top_performers(5)
        
        # Build report content
        report = f"""
📱 TIKTOK ANALYTICS REPORT
{'═' * 50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Device: Termux Android
Total Videos Analyzed: {stats['total_videos']}

📊 OVERVIEW STATISTICS
{'─' * 30}
📹 Total Videos: {stats['total_videos']:,}
👀 Total Views: {stats['total_views']:,}
❤️ Total Likes: {stats['total_likes']:,}
💬 Total Comments: {stats['total_comments']:,}
🔄 Total Shares: {stats['total_shares']:,}
👥 Followers Gained: {stats['total_followers']:,}

📈 PERFORMANCE METRICS
{'─' * 35}
Average Views per Video: {stats['avg_views']:,.0f}
Average Engagement Rate: {stats['avg_engagement_rate']:.2f}%
Best Performing Video: {stats['best_video_id']}
Best Video Views: {stats['best_video_views']:,}
Best Video Category: {stats['best_video_category']}

🎯 KEY INSIGHTS
{'─' * 25}
"""
        
        for i, insight in enumerate(insights, 1):
            report += f"{i}. {insight}\n"
        
        # Add category performance chart
        if categories:
            category_views = {cat: data['avg_views'] for cat, data in categories.items()}
            report += self.create_simple_chart(category_views, "AVERAGE VIEWS BY CATEGORY")
        
        # Add top performers
        report += f"\n🏆 TOP 5 PERFORMING VIDEOS\n{'─' * 40}\n"
        for i, video in enumerate(top_videos, 1):
            total_eng = video['likes'] + video['comments'] + video['shares']
            eng_rate = (total_eng / video['views']) * 100 if video['views'] > 0 else 0
            report += f"{i}. {video['id']} ({video['category']})\n"
            report += f"   Views: {video['views']:,} | Engagement: {eng_rate:.1f}%\n"
            report += f"   Duration: {video['duration']}s | Hashtags: {video['hashtags']}\n\n"
        
        # Detailed category breakdown
        if categories:
            report += f"\n📋 DETAILED CATEGORY ANALYSIS\n{'─' * 45}\n"
            for cat, data in sorted(categories.items(), key=lambda x: x[1]['avg_engagement_rate'], reverse=True):
                report += f"\n{cat.upper()}:\n"
                report += f"  📹 Videos: {data['count']}\n"
                report += f"  👀 Total Views: {data['total_views']:,}\n"
                report += f"  📊 Avg Views: {data['avg_views']:,.0f}\n"
                report += f"  💝 Engagement Rate: {data['avg_engagement_rate']:.2f}%\n"
        
        report += f"""
💡 RECOMMENDATIONS
{'─' * 30}
1. Create more content in your best-performing category
2. Optimize video duration based on insights above
3. Use the recommended number of hashtags
4. Post at optimal times for better reach
5. Analyze your top videos for common success factors

📄 Report saved to: {filename}
🔧 Generated by Termux TikTok Analytics Tool
"""
        
        # Save report
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Report saved: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
    
    def print_quick_summary(self):
        """Print quick summary to terminal"""
        stats = self.calculate_basic_stats()
        if not stats:
            print("❌ No data available")
            return
        
        print(f"\n📱 QUICK TIKTOK SUMMARY")
        print(f"{'═' * 35}")
        print(f"📹 Videos: {stats['total_videos']}")
        print(f"👀 Total Views: {stats['total_views']:,}")
        print(f"❤️ Total Likes: {stats['total_likes']:,}")
        print(f"📊 Avg Engagement: {stats['avg_engagement_rate']:.1f}%")
        print(f"🏆 Best Video: {stats['best_video_id']} ({stats['best_video_views']:,} views)")
        
        insights = self.generate_insights()
        if insights:
            print(f"\n🎯 TOP INSIGHTS:")
            for insight in insights[:3]:  # Show top 3 insights
                print(f"  • {insight}")

def main():
    """Main function optimized for Termux"""
    print("📱 TERMUX TIKTOK ANALYTICS")
    print("═" * 40)
    print("🤖 Android-optimized TikTok report generator")
    
    reporter = TermuxTikTokReporter()
    
    # Check if user has existing data
    print(f"\n📂 Working directory: {reporter.storage_path}")
    
    choice = input("\n🔄 Choose data source:\n1. Generate sample data\n2. Load existing JSON file\nEnter choice (1-2): ").strip()
    
    if choice == "2":
        filename = input("📄 Enter JSON filename (or press Enter for 'tiktok_data.json'): ").strip()
        if not filename:
            filename = "tiktok_data.json"
        
        if not reporter.load_from_json(filename):
            print("⚠️ Could not load file. Generating sample data instead...")
            reporter.create_sample_data()
            reporter.save_sample_json()
    else:
        print("📊 Generating sample data...")
        num_videos = input("📹 Number of sample videos (default 30): ").strip()
        try:
            num_videos = int(num_videos) if num_videos else 30
        except:
            num_videos = 30
        
        reporter.create_sample_data(num_videos)
        reporter.save_sample_json()
    
    # Show quick summary
    reporter.print_quick_summary()
    
    # Generate full report
    generate_full = input(f"\n📄 Generate full report? (y/n): ").strip().lower()
    if generate_full in ['y', 'yes', '']:
        print(f"\n📝 Generating comprehensive report...")
        if reporter.generate_report():
            print(f"✅ Report generation complete!")
        else:
            print(f"❌ Failed to generate report")
    
    print(f"\n🎉 Analysis complete!")
    print(f"📁 Check your files in: {reporter.storage_path}")

if __name__ == "__main__":
    main()
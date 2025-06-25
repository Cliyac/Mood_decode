#!/usr/bin/env python3
"""
Interactive Testing Interface for MoodDecode API
Allows users to input their own text and test all endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"  # Change to your ngrok URL when deployed


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header():
    """Print welcome header"""
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}           MoodDecode API - Interactive Tester{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.CYAN}Test your NLP API endpoints with custom input!{Colors.END}")
    print()


def check_server():
    """Check if the API server is running"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✓ Server is running at {BASE_URL}{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ Server responded with status {response.status_code}{Colors.END}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}✗ Could not connect to server at {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Make sure your Flask app is running!{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ Error checking server: {e}{Colors.END}")
        return False


def get_user_input():
    """Get text input from user"""
    print(f"{Colors.BOLD}Enter your text (or 'quit' to exit):{Colors.END}")
    print(f"{Colors.CYAN}> {Colors.END}", end="")
    user_input = input().strip()
    return user_input


def test_mood_analysis(text):
    """Test mood analysis endpoint with user input"""
    try:
        response = requests.post(f"{BASE_URL}/analyze_mood",
                                 json={"text": text},
                                 timeout=10)

        if response.status_code == 200:
            result = response.json()
            emotion = result.get('emotion', 'Unknown')

            # Color code emotions
            emotion_colors = {
                'happy': Colors.GREEN,
                'sad': Colors.BLUE,
                'angry': Colors.RED,
                'fear': Colors.YELLOW,
                'surprise': Colors.CYAN,
                'disgust': Colors.RED,
                'neutral': Colors.END
            }

            color = emotion_colors.get(emotion, Colors.END)
            print(f"  {Colors.BOLD}Emotion:{Colors.END} {color}{emotion.upper()}{Colors.END}")

        else:
            error_data = response.json() if response.headers.get(
                'content-type') == 'application/json' else response.text
            print(f"  {Colors.RED}Error: {response.status_code} - {error_data}{Colors.END}")

    except Exception as e:
        print(f"  {Colors.RED}Error: {e}{Colors.END}")


def test_crisis_detection(text):
    """Test crisis detection endpoint with user input"""
    try:
        response = requests.post(f"{BASE_URL}/detect_crisis",
                                 json={"text": text},
                                 timeout=10)

        if response.status_code == 200:
            result = response.json()
            crisis_detected = result.get('crisis_detected', False)

            if crisis_detected:
                print(f"  {Colors.BOLD}Crisis Status:{Colors.END} {Colors.RED}⚠️  CRISIS DETECTED{Colors.END}")
                print(f"  {Colors.YELLOW}Note: If this is a real crisis, please seek immediate help!{Colors.END}")
            else:
                print(f"  {Colors.BOLD}Crisis Status:{Colors.END} {Colors.GREEN}✓ No crisis detected{Colors.END}")

        else:
            error_data = response.json() if response.headers.get(
                'content-type') == 'application/json' else response.text
            print(f"  {Colors.RED}Error: {response.status_code} - {error_data}{Colors.END}")

    except Exception as e:
        print(f"  {Colors.RED}Error: {e}{Colors.END}")


def test_summarization(text):
    """Test text summarization endpoint with user input"""
    try:
        response = requests.post(f"{BASE_URL}/summarize",
                                 json={"text": text},
                                 timeout=10)

        if response.status_code == 200:
            result = response.json()
            summary = result.get('summary', 'No summary available')

            print(f"  {Colors.BOLD}Original Length:{Colors.END} {len(text)} characters")
            print(f"  {Colors.BOLD}Summary Length:{Colors.END} {len(summary)} characters")
            print(f"  {Colors.BOLD}Compression:{Colors.END} {((len(text) - len(summary)) / len(text) * 100):.1f}%")
            print(f"  {Colors.BOLD}Summary:{Colors.END}")
            print(f"  {Colors.CYAN}\"{summary}\"{Colors.END}")

        else:
            error_data = response.json() if response.headers.get(
                'content-type') == 'application/json' else response.text
            print(f"  {Colors.RED}Error: {response.status_code} - {error_data}{Colors.END}")

    except Exception as e:
        print(f"  {Colors.RED}Error: {e}{Colors.END}")


def show_menu():
    """Display testing menu"""
    print(f"\n{Colors.BOLD}Choose what to test:{Colors.END}")
    print(f"  {Colors.CYAN}1{Colors.END} - Mood Analysis only")
    print(f"  {Colors.CYAN}2{Colors.END} - Crisis Detection only")
    print(f"  {Colors.CYAN}3{Colors.END} - Text Summarization only")
    print(f"  {Colors.CYAN}4{Colors.END} - Test ALL endpoints")
    print(f"  {Colors.CYAN}5{Colors.END} - Change server URL")
    print(f"  {Colors.CYAN}q{Colors.END} - Quit")
    print(f"{Colors.YELLOW}Enter your choice: {Colors.END}", end="")


def change_server_url():
    """Allow user to change the server URL"""
    global BASE_URL
    print(f"\n{Colors.BOLD}Current server URL: {Colors.END}{BASE_URL}")
    print(f"{Colors.BOLD}Enter new server URL (or press Enter to keep current): {Colors.END}")
    new_url = input().strip()
    if new_url:
        # Remove trailing slash if present
        BASE_URL = new_url.rstrip('/')
        print(f"{Colors.GREEN}✓ Server URL updated to: {BASE_URL}{Colors.END}")


def run_tests(text, choice):
    """Run the selected tests"""
    print(f"\n{Colors.BOLD}{'=' * 50}{Colors.END}")
    print(f"{Colors.BOLD}Testing with text: {Colors.END}\"{text}\"")
    print(f"{Colors.BOLD}Timestamp: {Colors.END}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.BOLD}{'=' * 50}{Colors.END}")

    if choice in ['1', '4']:
        print(f"\n{Colors.BOLD}🎭 MOOD ANALYSIS:{Colors.END}")
        test_mood_analysis(text)

    if choice in ['2', '4']:
        print(f"\n{Colors.BOLD}🚨 CRISIS DETECTION:{Colors.END}")
        test_crisis_detection(text)

    if choice in ['3', '4']:
        print(f"\n{Colors.BOLD}📝 TEXT SUMMARIZATION:{Colors.END}")
        test_summarization(text)


def show_sample_inputs():
    """Show sample inputs for testing"""
    print(f"\n{Colors.BOLD}Sample inputs you can try:{Colors.END}")
    print(f"{Colors.CYAN}Happy:{Colors.END} I'm absolutely thrilled about my promotion!")
    print(f"{Colors.CYAN}Sad:{Colors.END} I feel so lonely and depressed lately")
    print(f"{Colors.CYAN}Crisis:{Colors.END} I can't take it anymore, I want to hurt myself")
    print(f"{Colors.CYAN}Long text:{Colors.END} Artificial intelligence is transforming our world...")
    print()


def main():
    """Main interactive testing loop"""
    print_header()

    # Check if server is running
    if not check_server():
        print(f"\n{Colors.YELLOW}Please start your Flask server first:{Colors.END}")
        print(f"  python app.py")
        print(f"\n{Colors.YELLOW}Or update the server URL if using ngrok{Colors.END}")
        return

    show_sample_inputs()

    while True:
        try:
            show_menu()
            choice = input().strip().lower()

            if choice == 'q' or choice == 'quit':
                print(f"\n{Colors.GREEN}Thanks for testing MoodDecode API! 👋{Colors.END}")
                break

            elif choice == '5':
                change_server_url()
                if not check_server():
                    continue

            elif choice in ['1', '2', '3', '4']:
                text = get_user_input()

                if text.lower() in ['quit', 'q', 'exit']:
                    print(f"\n{Colors.GREEN}Thanks for testing MoodDecode API! 👋{Colors.END}")
                    break

                if not text:
                    print(f"{Colors.RED}Please enter some text to analyze{Colors.END}")
                    continue

                run_tests(text, choice)

                # Ask if user wants to continue
                print(f"\n{Colors.YELLOW}Press Enter to continue testing or 'q' to quit: {Colors.END}", end="")
                continue_choice = input().strip().lower()
                if continue_choice in ['q', 'quit']:
                    print(f"\n{Colors.GREEN}Thanks for testing MoodDecode API! 👋{Colors.END}")
                    break

            else:
                print(f"{Colors.RED}Invalid choice. Please enter 1-5 or 'q'{Colors.END}")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}Thanks for testing MoodDecode API! 👋{Colors.END}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")


if __name__ == "__main__":
    main()
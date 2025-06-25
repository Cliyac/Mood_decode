#!/usr/bin/env python3
"""
Test script for MoodDecode API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"  # Change this to your ngrok URL when deployed


def test_mood_analysis():
    """Test the mood analysis endpoint"""
    print("Testing Mood Analysis Endpoint...")
    print("-" * 40)

    test_cases = [
        "I feel amazing today!",
        "I am so sad and depressed",
        "This makes me really angry and frustrated",
        "I'm scared about what might happen",
        "What a wonderful surprise this is!",
        "This is disgusting and revolting",
        "I feel okay, nothing special"
    ]

    for text in test_cases:
        response = requests.post(f"{BASE_URL}/analyze_mood",
                                 json={"text": text})
        if response.status_code == 200:
            result = response.json()
            print(f"Text: '{text}'")
            print(f"Emotion: {result['emotion']}")
            print()
        else:
            print(f"Error: {response.status_code} - {response.text}")


def test_crisis_detection():
    """Test the crisis detection endpoint"""
    print("Testing Crisis Detection Endpoint...")
    print("-" * 40)

    test_cases = [
        "I'm feeling hopeless and might hurt myself",
        "I want to end my life, there's no point in living",
        "I'm having a great day at work",
        "I can't go on anymore, I'm worthless",
        "Planning to meet friends for dinner",
        "I feel like a burden to everyone",
        "Excited about my vacation next week"
    ]

    for text in test_cases:
        response = requests.post(f"{BASE_URL}/detect_crisis",
                                 json={"text": text})
        if response.status_code == 200:
            result = response.json()
            print(f"Text: '{text}'")
            print(f"Crisis Detected: {result['crisis_detected']}")
            print()
        else:
            print(f"Error: {response.status_code} - {response.text}")


def test_summarization():
    """Test the text summarization endpoint"""
    print("Testing Text Summarization Endpoint...")
    print("-" * 40)

    long_text = """
    Artificial Intelligence has revolutionized the way we interact with technology and process information. 
    Machine learning algorithms have become increasingly sophisticated, enabling computers to perform tasks 
    that were once thought to be exclusively human. Natural Language Processing is a particularly exciting 
    field that allows machines to understand and generate human language. Deep learning models like neural 
    networks have shown remarkable success in various applications including image recognition, speech 
    processing, and text analysis. The future of AI holds immense potential for solving complex problems 
    in healthcare, education, transportation, and many other domains. However, it's important to consider 
    the ethical implications and ensure responsible development of these powerful technologies. As we move 
    forward, collaboration between researchers, policymakers, and industry leaders will be crucial for 
    harnessing the benefits of AI while mitigating potential risks.
    """

    response = requests.post(f"{BASE_URL}/summarize",
                             json={"text": long_text})
    if response.status_code == 200:
        result = response.json()
        print(f"Original text length: {len(long_text)} characters")
        print(f"Summary length: {len(result['summary'])} characters")
        print(f"\nOriginal text: {long_text.strip()}")
        print(f"\nSummary: {result['summary']}")
        print()
    else:
        print(f"Error: {response.status_code} - {response.text}")


def test_error_handling():
    """Test error handling"""
    print("Testing Error Handling...")
    print("-" * 40)

    # Test missing text field
    response = requests.post(f"{BASE_URL}/analyze_mood", json={})
    print(f"Missing text field - Status: {response.status_code}, Response: {response.json()}")

    # Test empty text
    response = requests.post(f"{BASE_URL}/analyze_mood", json={"text": ""})
    print(f"Empty text - Status: {response.status_code}, Response: {response.json()}")

    # Test invalid endpoint
    response = requests.post(f"{BASE_URL}/invalid_endpoint", json={"text": "test"})
    print(f"Invalid endpoint - Status: {response.status_code}, Response: {response.json()}")

    print()


def main():
    """Run all tests"""
    print("=" * 50)
    print("MoodDecode API Testing")
    print("=" * 50)
    print()

    try:
        # Test if server is running
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("Error: Server is not running or not accessible")
            print(f"Make sure the Flask app is running on {BASE_URL}")
            return

        print("Server is running! Starting tests...\n")

        test_mood_analysis()
        test_crisis_detection()
        test_summarization()
        test_error_handling()

        print("All tests completed!")

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to server at {BASE_URL}")
        print("Make sure the Flask app is running and the URL is correct")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
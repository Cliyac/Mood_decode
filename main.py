#!/usr/bin/env python3
"""
MoodDecode: NLP API for Emotion Analysis, Crisis Detection, and Text Summarization
"""

from flask import Flask, request, jsonify
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import heapq
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize NLTK components
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MoodAnalyzer:
    """Analyzes mood/emotion from text using NLTK VADER and custom rules"""

    def __init__(self):
        # Define emotion keywords for better classification
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'amazing', 'wonderful', 'great', 'fantastic', 'awesome', 'pleased',
                      'delighted'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'gloomy', 'down', 'blue', 'melancholy'],
            'angry': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'rage', 'upset', 'frustrated'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous', 'panic', 'frightened'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'unexpected'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sick', 'nauseated', 'appalled']
        }

    def analyze_emotion(self, text):
        """Analyze emotion from text"""
        text_lower = text.lower()

        # Get VADER sentiment scores
        scores = sia.polarity_scores(text)

        # Count emotion keywords
        emotion_counts = {}
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotion_counts[emotion] = count

        # Determine emotion based on keywords and sentiment
        if emotion_counts:
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            return dominant_emotion

        # Fallback to sentiment analysis
        compound_score = scores['compound']
        if compound_score >= 0.5:
            return 'happy'
        elif compound_score <= -0.5:
            return 'sad'
        elif compound_score <= -0.1:
            return 'sad'
        elif compound_score >= 0.1:
            return 'happy'
        else:
            return 'neutral'


class CrisisDetector:
    """Detects crisis situations from text using keyword matching and sentiment analysis"""

    def __init__(self):
        # Crisis keywords (self-harm, suicide, violence indicators)
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'hurt myself', 'self harm',
            'want to die', 'better off dead', 'no point living', 'hopeless',
            'can\'t go on', 'end it all', 'take my life', 'harm myself',
            'cut myself', 'overdose', 'jump off', 'hanging myself',
            'worthless', 'useless', 'burden', 'everyone would be better',
            'plan to hurt', 'plan to kill', 'thoughts of death'
        ]

        # Severity weights for different phrases
        self.severity_weights = {
            'suicide': 0.9,
            'kill myself': 0.9,
            'hurt myself': 0.7,
            'hopeless': 0.6,
            'worthless': 0.5,
            'can\'t go on': 0.7,
            'want to die': 0.8
        }

    def detect_crisis(self, text):
        """Detect if text indicates a crisis situation"""
        text_lower = text.lower()

        # Check for direct crisis keywords
        crisis_score = 0
        found_keywords = []

        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
                crisis_score += self.severity_weights.get(keyword, 0.5)

        # Get sentiment analysis
        scores = sia.polarity_scores(text)

        # Combine keyword detection with extreme negative sentiment
        if found_keywords or (scores['compound'] <= -0.8 and scores['neg'] >= 0.6):
            return True

        # Additional check for high crisis score
        if crisis_score >= 0.7:
            return True

        return False


class TextSummarizer:
    """Summarizes text using extractive summarization"""

    def __init__(self):
        pass

    def summarize(self, text, max_sentences=3):
        """Create extractive summary of text"""
        # Tokenize into sentences
        sentences = sent_tokenize(text)

        # If text is short, return as is
        if len(sentences) <= max_sentences:
            return text.strip()

        # Calculate sentence scores based on word frequency
        word_freq = self._calculate_word_frequency(text)
        sentence_scores = self._score_sentences(sentences, word_freq)

        # Get top sentences
        top_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)

        # Sort by original order and join
        top_sentences.sort(key=lambda x: sentences.index(x))
        summary = ' '.join(top_sentences)

        return summary.strip()

    def _calculate_word_frequency(self, text):
        """Calculate word frequency for scoring"""
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]
        return Counter(words)

    def _score_sentences(self, sentences, word_freq):
        """Score sentences based on word frequency"""
        sentence_scores = {}

        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word.isalnum() and word not in stop_words]

            if len(words) > 0:
                score = sum(word_freq.get(word, 0) for word in words) / len(words)
                sentence_scores[sentence] = score

        return sentence_scores


# Initialize analyzers
mood_analyzer = MoodAnalyzer()
crisis_detector = CrisisDetector()
text_summarizer = TextSummarizer()


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "MoodDecode NLP API",
        "version": "1.0",
        "endpoints": {
            "POST /analyze_mood": "Analyze emotion from text",
            "POST /detect_crisis": "Detect crisis situations",
            "POST /summarize": "Summarize text content"
        },
        "example_usage": {
            "analyze_mood": {
                "input": {"text": "I feel amazing today!"},
                "output": {"emotion": "happy"}
            },
            "detect_crisis": {
                "input": {"text": "I'm feeling hopeless and might hurt myself"},
                "output": {"crisis_detected": True}
            },
            "summarize": {
                "input": {"text": "Long paragraph here..."},
                "output": {"summary": "Condensed version..."}
            }
        }
    })


@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    """Analyze mood/emotion from input text"""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400

        text = data['text']
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400

        emotion = mood_analyzer.analyze_emotion(text)

        logger.info(f"Mood analysis - Input: {text[:50]}... -> Emotion: {emotion}")

        return jsonify({"emotion": emotion})

    except Exception as e:
        logger.error(f"Error in mood analysis: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/detect_crisis', methods=['POST'])
def detect_crisis():
    """Detect crisis situations from input text"""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400

        text = data['text']
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400

        crisis_detected = crisis_detector.detect_crisis(text)

        logger.info(f"Crisis detection - Input: {text[:50]}... -> Crisis: {crisis_detected}")

        return jsonify({"crisis_detected": crisis_detected})

    except Exception as e:
        logger.error(f"Error in crisis detection: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/summarize', methods=['POST'])
def summarize():
    """Summarize input text"""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400

        text = data['text']
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400

        summary = text_summarizer.summarize(text)

        logger.info(f"Text summarization - Input length: {len(text)} -> Summary length: {len(summary)}")

        return jsonify({"summary": summary})

    except Exception as e:
        logger.error(f"Error in text summarization: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == '__main__':
    print("Starting MoodDecode NLP API...")
    print("Available endpoints:")
    print("  POST /analyze_mood - Analyze emotion from text")
    print("  POST /detect_crisis - Detect crisis situations")
    print("  POST /summarize - Summarize text content")
    print("\nServer starting on http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)
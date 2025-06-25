# Team CIPHER

## 🧠 Project Description

An NLP-based backend service with three main endpoints designed to analyze mood, detect crisis-level text, and summarize user input — simulating real-world mental health tools and smart journaling assistants.

## 🚀 Endpoints & Logic

### 1. POST /analyze-mood

* *Purpose:* Detect the emotion in the given text.
* *Logic Used:*
  This endpoint uses the NLTK VADER sentiment analyzer (SentimentIntensityAnalyzer) along with custom keyword-based emotion mapping. It scans the text for emotion-specific keywords and prioritizes that match. If no keyword dominates, it uses the compound sentiment score to return an emotion (happy, sad, or neutral).
* *Sample Input:*

json
{ "text": "I feel amazing today!" }


* *Sample Output:*

json
{ "emotion": "happy" }


---

### 2. POST /detect-crisis

* *Purpose:* Detects if the text indicates a mental health crisis.
* *Logic Used:*
  A list of high-risk phrases is used alongside severity weights. If any keywords like "suicide" or "hurt myself" are found in the text, a cumulative crisis score is calculated. The system also cross-checks with sentiment values (e.g., compound ≤ -0.8 and neg ≥ 0.6). If either condition is triggered, it flags the input as a crisis.
* *Sample Input:*

json
{ "text": "I'm feeling hopeless and might hurt myself" }


* *Sample Output:*

json
{ "crisis_detected": true }


---

### 3. POST /summarize

* *Purpose:* Summarize long text into a short version.
* *Logic Used:*
  Implements an extractive summarization method. The input is tokenized into sentences and words. Stopwords are removed, word frequency is calculated, and each sentence is scored. The top 3 highest-scoring sentences are returned in original order as the summary.
* *Sample Input:*

json
{ "text": "Today was a really long day full of meetings, deadlines, and emotional stress..." }


* *Sample Output:*

json
{ "summary": "It was a stressful and exhausting day." }


---

## 🧰 Tech Stack

* *Backend:* Flask
* *Model/API:* Custom-trained model using Python and NLTK
* *Hosting:* Ngrok

## 🔗 API Access

* *Base URL:* https://5c20-34-106-64-117.ngrok-free.app
* *Endpoints:*

  * POST /analyze_mood: [https://5c20-34-106-64-117.ngrok-free.app/analyze\_mood](https://5c20-34-106-64-117.ngrok-free.app/analyze_mood)
  * POST /detect_crisis: [https://5c20-34-106-64-117.ngrok-free.app/detect\_crisis](https://5c20-34-106-64-117.ngrok-free.app/detect_crisis)
  * POST /summarize: [https://5c20-34-106-64-117.ngrok-free.app/summarize](https://5c20-34-106-64-117.ngrok-free.app/summarize)

---

"""
chatbot_model.py
================
Core NLP engine for the AI Smart Chatbot.

Uses:
- NLTK for text preprocessing (tokenization, lemmatization, stopword removal)
- scikit-learn for TF-IDF vectorization
- NumPy + cosine similarity for response matching
- difflib for fuzzy spelling correction
"""

import json
import random
import re
import difflib
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ──────────────────────────────────────────────
# Download required NLTK resources (runs once)
# ──────────────────────────────────────────────
def download_nltk_resources():
    """Download all required NLTK data packages silently."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]
    for path, pkg in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)

download_nltk_resources()


# ──────────────────────────────────────────────
# ChatbotModel class
# ──────────────────────────────────────────────
class ChatbotModel:
    """
    Main chatbot engine.

    Steps:
    1. Load intents from intents.json
    2. Preprocess all patterns using NLP
    3. Vectorize patterns with TF-IDF
    4. At query time: preprocess input → vectorize → find best match via cosine similarity
    5. Return a random response from the matched intent
    """

    def __init__(self, intents_path: str = "intents.json"):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        # Load intent data
        with open(intents_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.intents = data["intents"]

        # Build a flat list of (pattern, tag, responses) for vectorization
        self.patterns: list[str] = []
        self.tags: list[str] = []
        self.tag_to_responses: dict[str, list[str]] = {}

        for intent in self.intents:
            tag = intent["tag"]
            self.tag_to_responses[tag] = intent["responses"]
            for pattern in intent["patterns"]:
                self.patterns.append(pattern)
                self.tags.append(tag)

        # Preprocess patterns and fit TF-IDF vectorizer
        self.processed_patterns = [self._preprocess(p) for p in self.patterns]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),   # unigrams + bigrams for better matching
            min_df=1,
            analyzer="word",
        )
        self.pattern_vectors = self.vectorizer.fit_transform(self.processed_patterns)

        # Vocabulary for spelling correction
        self.vocab = list(self.vectorizer.vocabulary_.keys())

    # ──────────────────────────────────────────
    # Text Preprocessing
    # ──────────────────────────────────────────
    def _preprocess(self, text: str) -> str:
        """
        Full NLP preprocessing pipeline:
        1. Lowercase
        2. Remove special characters
        3. Tokenize
        4. Remove stopwords (keep negations like 'not', 'no')
        5. Lemmatize
        """
        # Lowercase
        text = text.lower().strip()

        # Remove special characters, keep apostrophes for contractions
        text = re.sub(r"[^a-zA-Z0-9\s']", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Tokenize
        tokens = word_tokenize(text)

        # Negation words to preserve
        negations = {"not", "no", "never", "none", "nobody", "nothing"}

        # Remove stopwords but keep negations
        tokens = [
            t for t in tokens
            if t not in self.stop_words or t in negations
        ]

        # Lemmatize each token
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]

        return " ".join(tokens) if tokens else text

    # ──────────────────────────────────────────
    # Spelling Correction
    # ──────────────────────────────────────────
    def _correct_spelling(self, text: str) -> str:
        """
        Light spelling correction using difflib.
        Replaces unknown words with the closest vocabulary match
        if similarity is above a threshold.
        """
        words = text.lower().split()
        corrected = []
        for word in words:
            # Only try to correct words longer than 3 characters
            if len(word) > 3 and word not in self.vocab:
                matches = difflib.get_close_matches(word, self.vocab, n=1, cutoff=0.8)
                corrected.append(matches[0] if matches else word)
            else:
                corrected.append(word)
        return " ".join(corrected)

    # ──────────────────────────────────────────
    # Response Generation
    # ──────────────────────────────────────────
    def get_response(self, user_input: str, threshold: float = 0.15) -> tuple[str, float]:
        """
        Main inference method.

        Args:
            user_input: Raw text from the user.
            threshold:  Minimum cosine similarity to accept a match.

        Returns:
            (response_text, confidence_score)
        """
        if not user_input.strip():
            return "Please type something so I can help you! 😊", 0.0

        # Apply spelling correction then preprocess
        corrected = self._correct_spelling(user_input)
        processed = self._preprocess(corrected)

        if not processed.strip():
            return self._fallback_response(), 0.0

        # Vectorize the input
        try:
            input_vector = self.vectorizer.transform([processed])
        except Exception:
            return self._fallback_response(), 0.0

        # Compute cosine similarity against all patterns
        similarities = cosine_similarity(input_vector, self.pattern_vectors).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        # If score is above threshold, return a response from the matched intent
        if best_score >= threshold:
            matched_tag = self.tags[best_idx]
            responses = self.tag_to_responses[matched_tag]
            return random.choice(responses), best_score

        # Below threshold → fallback
        return self._fallback_response(), best_score

    def _fallback_response(self) -> str:
        """Return a random fallback message when no good match is found."""
        fallbacks = [
            "🤔 Hmm, I'm not quite sure about that one. Could you rephrase or ask something else?",
            "😅 That's a tricky one! I'm still learning. Try asking about AI, coding, Python, or motivation!",
            "🧐 I didn't quite catch that. You can ask me about programming, AI, careers, or even request a joke!",
            "💭 Interesting question! I'm not sure I have the answer, but try rephrasing — I'm always improving!",
            "🤖 Beep boop... my circuits don't recognize that pattern yet! Ask me about tech, coding, or AI! 😄",
        ]
        return random.choice(fallbacks)

    def get_intent_count(self) -> int:
        """Return the number of loaded intents."""
        return len(self.intents)

    def get_pattern_count(self) -> int:
        """Return the total number of training patterns."""
        return len(self.patterns)

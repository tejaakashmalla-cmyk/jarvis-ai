import re


class IntentAnalyzer:

    def __init__(self):

        self.intent_patterns = {
            "memory": [
                r"\bremember\b",
                r"\bstore\b",
                r"\bsave\b",
                r"\bdon't forget\b",
                r"\bmy name\b",
                r"\bfavorite\b",
                r"\bi like\b",
                r"\bi love\b",
                r"\bi prefer\b"
            ],

            "coding": [
                r"\bpython\b",
                r"\bjava\b",
                r"\bc\+\+\b",
                r"\bjavascript\b",
                r"\breact\b",
                r"\bhtml\b",
                r"\bcss\b",
                r"\bnode\b",
                r"\bbug\b",
                r"\berror\b",
                r"\bfix\b",
                r"\bdebug\b",
                r"\bprogram\b",
                r"\bcode\b"
            ],

            "tool": [
                r"\bopen\b",
                r"\blaunch\b",
                r"\bstart\b",
                r"\bclose\b",
                r"\brun\b",
                r"\bshutdown\b",
                r"\brestart\b"
            ],

            "document": [
                r"\bpdf\b",
                r"\bfile\b",
                r"\bdocument\b",
                r"\bresume\b",
                r"\bnotes\b",
                r"\bread\b",
                r"\bsummarize\b"
            ]
        }

    def detect(self, text):

        text = text.lower()

        for intent, patterns in self.intent_patterns.items():

            for pattern in patterns:

                if re.search(pattern, text):

                    return {
                        "intent": intent,
                        "confidence": 0.95
                    }

        return {
            "intent": "chat",
            "confidence": 0.80
        }
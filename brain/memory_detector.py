from memory.extractors.basic_extractor import BasicExtractor


class MemoryDetector:

    def __init__(self):

        self.extractor = BasicExtractor()

    def extract(self, text):

        return self.extractor.extract(text)
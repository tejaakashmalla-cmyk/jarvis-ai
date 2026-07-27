class ResponsePipeline:

    def process_token(self, token):

        # Future:
        # - Markdown formatting
        # - Emoji handling
        # - Code formatting
        # - Safety filtering

        return token

    def finalize(self, response):

        return response.strip()
import os
import openai
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class chat_gpt_question_ans:

    def __init__(self, model_engine="text-davinci-003"):
        openai.api_key = os.environ.get("OPENAPI_KEY")
        self.model_engine = model_engine

    def ask_query_with_one_answer(self, prompt: str):
        try:
            # logging.info("==========================prompt==========================")
            # logging.info(prompt)
            response = self.ask_query(prompt)
            if not response:
                logging.info("==========================Empty Response==========================")
                return response
            return response.choices[0].text.strip()

        except Exception as ex:
            logging.error("Exception in ask_query_with_one_answer")
            logging.error(ex)

    def ask_query_with_multiple_answer(self, prompt: str, n: int = 1):
        try:
            response = self.ask_query(prompt, n)
            result = ""
            if not response:
                logging.info("==========================Empty Response==========================")
                return result
            for choice in response.choices:
                result += choice.text
            return result
        except Exception as ex:
            logging.error("Exception in ask_query_with_multiple_answer")
            logging.error(ex)

    def ask_query(self, prompt: str, n: int = 1):
        try:
            logging.info("==========================prompt==========================")
            logging.info(prompt)
            response = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5,
                n=n
            )
            return response
        except Exception as ex:
            logging.error("Exception in ask_query")
            logging.error(ex)

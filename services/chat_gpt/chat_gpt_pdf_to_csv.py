import csv
import copy
import logging
import time
from random import randrange

from services.fileManagement import read_pdf
from services.chat_gpt.chat_gpt_question_ans import chat_gpt_question_ans
from services.mcq_converter import mcq_converter
from utils.constants import DEFAULT_CSV_HEADER

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def convert_pdf_to_csv():
    pdf_data = read_pdf.read_all_pdf()
    chat_gpt_question_ans_obj = chat_gpt_question_ans()

    for pdf_file in pdf_data:
        file_name = pdf_file.get('file_path')
        pdf_reader = pdf_file.get('file_data')
        csv_writer = mcq_converter()
        file_path = file_name.replace('.pdf', '.csv')
        csv_file = open(file_path, 'w', newline='', encoding='UTF-8', errors='ignore')
        writer = csv.DictWriter(csv_file, fieldnames=DEFAULT_CSV_HEADER)
        writer.writeheader()

        for page_data in pdf_reader:
            prompt = "make 5 question with 4 options with explanation from the data given " + page_data
            sleep_time = randrange(10)
            time.sleep(sleep_time/10)
            response = chat_gpt_question_ans_obj.ask_query_with_one_answer(prompt)
            if not response:
                continue
            logging.info("==========================chat gpt response==========================")
            logging.info(response)
            response_lines = response.split("\n")
            for current_text in response_lines:
                if csv_writer.prepare_row(current_text):
                    try:
                        if csv_writer.is_something_missing():
                            csv_writer.wrong_questions.append(copy.deepcopy(csv_writer.row_dict))
                        logging.info("<===========FINAL===========>")
                        logging.info(csv_writer.row_dict)
                        writer.writerow(csv_writer.row_dict)
                        # row_dict = init_dict.copy()
                        csv_writer.init_row_dict()
                    except Exception as ex:
                        csv_writer.write_to_csv_exceptions.append(copy.deepcopy(csv_writer.row_dict))
                        logging.error("Exception while writing to csv")
                        logging.error(csv_writer.row_dict)
                        logging.error(ex)

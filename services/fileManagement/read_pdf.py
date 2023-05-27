import os
import logging
from utils.constants import DEFAULT_FILE_PATH

# import PyPDF2
import fitz

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def read_all_pdf(path: str = DEFAULT_FILE_PATH):
    os.chdir(path)
    cwd = os.getcwd()
    logging.info(cwd)
    pdf_data = []
    for i in os.walk(cwd):
        for j in i[2]:
            if j.endswith('.pdf'):
                logging.info('File Name : %s', j)
                file_data = read_pdf(j)
                pdf_data.append({
                    "file_path": j,
                    "file_data": file_data
                })

    return pdf_data


def read_pdf(pdf_file):
    try:
        print(pdf_file)
        response = []
        # with open(pdf_file, 'rb') as f:
        #     # Create a PDF reader object
        #     pdf_reader = PyPDF2.PdfReader(f)
        #     return pdf_reader

        with fitz.open(pdf_file) as doc:
            for page in doc:
                response.append(page.get_text())
        return response
    except Exception as e:
        logging.error("Exception while read_pdf")
        logging.error(e)


def read_pdf_as_text(pdf_file):
    try:
        print(pdf_file)
        text = ""

        pdf_reader = read_pdf(pdf_file)

        # # Get the number of pages in the PDF file
        # num_pages = len(pdf_reader.pages)
        #
        # # Loop through each page and extract the text
        # for i in range(num_pages):
        #     page = pdf_reader.pages[i]
        #     text += page.extract_text()

        for page in pdf_reader:
            text += page

        return text
    except Exception as e:
        logging.error("Exception while read_pdf_as_text")
        logging.error(e)

import logging
from utils.constants import INIT_ROW_DICT, DEFAULT_CSV_COURSE, DEFAULT_CSV_TAGS, DEFAULT_CSV_TOPIC
from utils.mcq_utils.answer import answer
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def replace_string(text):
    text = text.replace("\n", "")
    text = text.replace("→", "->")
    text = text.replace("⟶", "->")
    text = text.replace("─", "-")
    text = text.replace("≥", ">=")
    text = text.replace("≤", "<=")
    text = text.replace("₂", "2")
    text = text.replace("²", "^2")
    text = text.replace("₃", "3")
    text = text.replace("³", "^3")
    text = text.replace("₄", "4")
    text = text.replace("₅", "5")
    text = text.replace("₆", "6")
    text = text.replace("₇", "7")
    text = text.replace("₈", "8")
    text = text.replace("₁₀", "10")
    text = text.replace("⁻", "-")
    text = text.replace("‾", "-")
    text = text.replace("⁺²", "+2")
    text = text.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('–', '-')
    text = text.replace('…', '...')
    text = text.replace('₹', 'Rs.')
    text = text.replace('π', 'Pi.')
    text = text.replace('υ', 'v.')
    text = text.replace('Ω', 'Ohm')
    text = text.replace('∠', '<')
    text = text.strip()
    return text


class mcq_converter:
    def __init__(self):
        self.current_state = None
        self.course = ''
        self.tag = ''
        self.topic = ''
        self.row_dict = INIT_ROW_DICT.copy()
        self.wrong_questions = []
        self.write_to_csv_exceptions = []

    def __int__(self, csv_file_path):
        self.course = ''
        self.tag = ''
        self.topic = ''
        self.row_dict = INIT_ROW_DICT.copy()
        self.wrong_questions = []
        self.write_to_csv_exceptions = []

    def set_course(self, course):
        self.course = course
        self.row_dict['course/subject'] = self.course

    def set_tag(self, tag):
        self.tag = tag
        self.row_dict['tags(Coma Seprate)'] = self.tag

    def set_topic(self, topic):
        self.topic = topic
        self.row_dict['topic(Topic id)'] = self.topic

    def init_row_dict(self):
        self.current_state = None
        self.row_dict = INIT_ROW_DICT.copy()
        self.row_dict['course/subject'] = self.course or DEFAULT_CSV_COURSE
        self.row_dict['tags(Coma Seprate)'] = self.topic or DEFAULT_CSV_TAGS
        self.row_dict['topic(Topic id)'] = self.topic or DEFAULT_CSV_TOPIC

    def is_something_missing(self):
        if not self.row_dict['question']:
            return True
        if not self.row_dict['answer']:
            return True
        if not self.row_dict['option1']:
            return True
        if not self.row_dict['option2']:
            return True
        if not self.row_dict['option3']:
            return True
        if not self.row_dict['option4']:
            return True

    def prepare_row(self, current_text):
        try:
            if re.search("^(Q[0-9]{1}\.)", current_text):
                # row_dict['course/subject'] = prev_text
                self.current_state = 'question'
                self.row_dict['question'] = current_text[3:]
                logging.info("Question No. %s=================", current_text)
                return False
            if re.search("^(Q[0-9]{2}\.)", current_text):
                # row_dict['course/subject'] = prev_text
                self.current_state = 'question'
                self.row_dict['question'] = current_text[4:].strip()
                logging.info("Question No. %s=================", current_text)
                return False
            if re.search("^(Q[0-9]{3}\.)", current_text):
                # row_dict['course/subject'] = prev_text
                self.current_state = 'question'
                self.row_dict['question'] = current_text[5:].strip()
                logging.info("Question No. %s=================", current_text)
                return False

            if re.search('^(A\.|a\.|A\)|a\))', current_text):
                logging.info("(A)=================")
                self.current_state = 'option1'
                self.row_dict['option1'] = current_text[2:].strip()
                return False
            if re.search('^(B\.|b\.|B\)|b\))', current_text):
                logging.info("(B)=================")
                self.current_state = 'option2'
                self.row_dict['option2'] = current_text[2:].strip()
                return False
            if re.search('^(C\.|c\.|C\)|c\))', current_text):
                logging.info("(C)=================")
                self.current_state = 'option3'
                self.row_dict['option3'] = current_text[2:].strip()
                return False
            if re.search('^(D\.|d\.|D\)|d\))', current_text):
                logging.info("(D)=================")
                self.current_state = 'option4'
                self.row_dict['option4'] = current_text[2:].strip()
                return False

            if re.search('^Answer: ', current_text):
                self.current_state = 'answer'
                index = len('Answer:')
                answer_text = current_text[index:].strip()

                self.row_dict['answer'] = answer[answer_text[0]]
                logging.info("answer===== %s ============ %s", current_text, self.row_dict['answer'])
                if re.search('Explanation:', current_text):
                    logging.info("Explanation is in answer=================")
                    self.current_state = 'explanation'
                    index = len('Explanation:')
                    self.row_dict['explanation'] = current_text[index:].strip()
                    return True
                return False

            if re.search('^Explanation:', current_text):
                logging.info("Explanation=================")
                self.current_state = 'explanation'
                index = len('Explanation:')
                self.row_dict['explanation'] = current_text[index:].strip()
                return True

            self.check_repeat_option(current_text)

            return False
        except Exception as ex:
            logging.error("Exception in ex_v1")
            logging.error(ex)

    def check_repeat_option(self, current_text):
        if self.current_state == 'question':
            if self.row_dict['question']:
                self.row_dict['question'] += '\n' + current_text.strip()
            else:
                self.row_dict['question'] += current_text.strip()

        if self.current_state == 'option1':
            if self.row_dict['option1']:
                self.row_dict['option1'] += '\n' + current_text.strip()
            else:
                self.row_dict['option1'] += current_text.strip()

        if self.current_state == 'option2':
            if self.row_dict['option2']:
                self.row_dict['option2'] += '\n' + current_text.strip()
            else:
                self.row_dict['option2'] += current_text.strip()

        if self.current_state == 'option3':
            if self.row_dict['option3']:
                self.row_dict['option3'] += '\n' + current_text.strip()
            else:
                self.row_dict['option3'] += current_text.strip()

        if self.current_state == 'option4':
            if self.row_dict['option4']:
                self.row_dict['option4'] += '\n' + current_text.strip()
            else:
                self.row_dict['option4'] += current_text.strip()

        if self.current_state == 'explanation':
            if self.row_dict['explanation']:
                self.row_dict['explanation'] += '\n' + current_text.strip()
            else:
                self.row_dict['explanation'] += current_text.strip()

    def check_repeat_option_for_next(self, current_text):
        if self.current_state == 'question':
            if self.row_dict['question']:
                self.row_dict['question'] += '\n' + current_text.strip()
            else:
                self.row_dict['question'] += current_text.strip()

        if self.current_state == 'explanation':
            if self.row_dict['explanation']:
                self.row_dict['explanation'] += '\n' + current_text.strip()
            else:
                self.row_dict['explanation'] += current_text.strip()




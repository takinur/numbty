import spacy
from spacy.matcher import Matcher
import re
import pandas as pd
import sys
import fitz
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.corpus import stopwords
import os
import docx2txt
from datetime import datetime
from dateutil import relativedelta
import io
import json
from rich import print, print_json


class resumeExtraction(object):
    def __init__(self, resume):
        self.STOPWORDS = set(stopwords.words('english')+['``', "''"])
        # Education Degrees
        self.EDUCATION = [
            'BE', 'BSC', 'BS', 'MSC', 'HONOURS',
            'ME', 'MS', 'MIS', 'BCOM', 'BCS', 'BCA', 'MCA',
            'BTECH', 'MTECH', 'DIPLOMA', '12TH', '10TH',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'XTH',
            'XIITH', 'FE', 'SE', 'TE', 'BECHALORS', 'MASTERS', 'PHD'
        ]
        self.RESUME_SECTIONS_GRAD = [
            'accomplishments',
            'experience',
            'education',
            'education history',
            'interests',
            'projects',
            'professional experience',
            'work experience',
            'publications',
            'skills',
            'certifications',
            'objective',
            'profile',
            'career objective',
            'summary',
            'leadership'
        ]
        # Skills File
        self.data = pd.read_csv('assets/data/skillsDB.csv')
        self.SKILLS_DB = list(self.data.columns.values)
        # Natural Language and vocabulary
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)
        # Details to Return
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'education': None,
            'degree': None,
            'projects': None,
            'experience': None,
            'total_experience': None,
            'text': None,
        }
        self.__resume = resume
        # Resume Extension
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        # Get Raw Text
        self.__text_raw = self.__extract_text(self.__resume, '.' + ext)
        # Format Raw Text
        self.__text = ' '.join(self.__text_raw.split())

        # print(self.__text_raw)

    def __extract_text(self, file_path, extension):
        text = ''
        if extension == '.pdf':
            for page in fitz.open(file_path):
                text = text + str(page.get_text())
        elif extension == '.docx':
            try:
                temp = docx2txt.process(file_path)
                text = [line.replace('\t', ' ')
                        for line in temp.split('\n') if line]
                return ' '.join(text)
            except KeyError:
                return ' '
        elif extension == '.doc':
            # text = extract_text_from_doc(file_path)
            text = 'doc file'
        return text

    def get_extracted_data(self):
        text = self.__text
        raw_text = self.__text_raw
        # print (raw_text)
        self.__details['name'] = self.__extract_name(text)
        self.__details['mobile_number'] = self.__extract_mobile_number(text)
        self.__details['email'] = self.__extract_email(text)
        self.__details['skills'] = self.__extract_skills(text)
        self.__details['degree'] = self.__extract_education(text)
        # Text that is essential for further processing
        # self.__details['text'] = text
        raw_entity = self.__extract_entity_sections(raw_text)
        try:
            self.__details['experience'] = raw_entity['experience']
            self.__details['education'] = raw_entity['education']
            self.__details['projects'] = raw_entity['projects']
            self.__details['total_experience'] = self.__total_experience_year(
                raw_entity)
        except KeyError:
            pass

        return self.__details

    def __extract_name(self, resume_text):

        nlp_text = self.nlp(resume_text)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

        self.matcher.add('NAME', [pattern])

        matches = self.matcher(nlp_text)
        for _, start, end in matches:
            span = nlp_text[1-start:end]

            number_of_words = len(span.text.split())
            if number_of_words < 2:
                span = nlp_text[start:end]
                return span.text
            print(number_of_words)
            return span.text

    def __extract_mobile_number(self, text):
        mob_num_regex = r'''(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{6})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'''

        phone = re.findall(re.compile(mob_num_regex), text)

        if phone:
            number = ''.join(phone[0])
            if len(number) > 11:
                return '+' + number
            else:
                return number

    def __extract_email(self, email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    def __extract_education(self, resume_text):

        nlp_text = self.nlp(resume_text)
        # Sentence Tokenizer
        nlp_text = [str(sent).strip() for sent in nlp_text.sents]
        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,|(|)]', r'', tex)
                if tex.upper() in self.EDUCATION and tex not in self.STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]

        # Extract year of education
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education

    def __extract_skills(self, input_text):
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(input_text)

        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]

        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]

        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(
            map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

        # a set to keep the results in.
        found_skills = set()

        # search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in self.SKILLS_DB:
                found_skills.add(token)

        # search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in self.SKILLS_DB:
                found_skills.add(ngram)

        return found_skills

    def __extract_entity_sections(self, text):
        text_split = [i.strip() for i in text.split('\n')]
        # sections_in_resume = [i for i in text_split if i.lower() in text]
        entities = {}
        key = False
        for phrase in text_split:
            if len(phrase) == 1:
                p_key = phrase
            else:
                p_key = set(phrase.lower().split()) & set(
                    self.RESUME_SECTIONS_GRAD)
            try:
                p_key = list(p_key)[0]
            except IndexError:
                pass
            if p_key in self.RESUME_SECTIONS_GRAD:
                entities[p_key] = []
                key = p_key
            elif key and phrase.strip():
                entities[key].append(phrase)
        return entities

    def __total_experience_year(self, raw_entity):
        try:
            experience = raw_entity['experience']
            try:
                exp = round(
                    self.get_total_experience(experience) / 12,
                    2
                )
                totalExperience = exp
            except KeyError:
                totalExperience = 0
        except KeyError:
            totalExperience = 0
        return totalExperience

    def get_total_experience(self, experience_list):

        exp_ = []
        for line in experience_list:
            experience = re.search(
                r'(?P<fmonth>\w+.\d+)\s*(\D|to)\s*(?P<smonth>\w+.\d+|present)',
                line,
                re.I
            )
            if experience:
                exp_.append(experience.groups())
        total_exp = sum(
            [self.__get_number_of_months_from_dates(i[0], i[2]) for i in exp_]
        )
        total_experience_in_months = total_exp
        return total_experience_in_months

    def __get_number_of_months_from_dates(self, date1, date2):

        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%b %Y')
        try:
            if len(date1.split()[0]) > 3:
                date1 = date1.split()
                date1 = date1[0][:3] + ' ' + date1[1]
            if len(date2.split()[0]) > 3:
                date2 = date2.split()
                date2 = date2[0][:3] + ' ' + date2[1]
        except IndexError:
            return 0
        try:
            date1 = datetime.strptime(str(date1), '%b %Y')
            date2 = datetime.strptime(str(date2), '%b %Y')
            months_of_experience = relativedelta.relativedelta(date2, date1)
            months_of_experience = (months_of_experience.years
                                    * 12 + months_of_experience.months)
        except ValueError:
            return 0
        return months_of_experience



file_url = 'assets/test_resumes/T_001.pdf'
# file_url = 'assets/test_resumes/T_002.docx'
# file_url = 'assets/test_resumes/T_003.pdf'
# file_url = 'assets/test_resumes/T_004.pdf'


# Argument from command line
if __name__ == '__main__':
    #Length of arguments
    args_len = len(sys.argv)
    #Check if the number of arguments is correct
    if args_len > 1:
        file_url = sys.argv[1]

    #Extracted data from the resume class
    data = resumeExtraction(file_url).get_extracted_data()
    # returns as json object
    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    jdata = json.dumps(data, cls=SetEncoder)

    print_json(jdata)


# TODO
'''
Fix Name Entity ->> Text is not in the correct format ->> Google Collab
Fix Education Entity
Grab Social media links
Extract Text from DOC


'''

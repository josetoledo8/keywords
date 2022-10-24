import numpy as np
import pandas as pd
import PyPDF2 


def extract_text_from_pdf(pdf_file):
    # Creating a pdf file object 
    pdfFileObj = open(pdf_file, 'rb') 
        
    # Creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        
    # Get the number of pages
    number_of_pages = pdfReader.numPages

    # String on which will be concatenated all text
    sample_raw = ''

    # Loop on pdf pages
    for page_number in range(number_of_pages):

        # creating a page object 
        pageObj = pdfReader.getPage(page_number) 

        # extracting text from page 
        text_on_page = pageObj.extractText()

        sample_raw += text_on_page
        
    # closing the pdf file object 
    pdfFileObj.close()
    
    return sample_raw.lower()


def text_treatment(sample_raw):

    # Characters which could appear sided to a word, like apple! (fruit) 10%...
    for ponctuation in [':',',','.',';','(',')','!','?','"',"'",'[',']','%','_','/', '\\', '\n']:

        sample_raw = sample_raw.replace(ponctuation, '')

    sample_raw = sample_raw.split()

    # Grants that special characters will not appear as a list element
    special_character = ['!','@','#','$','%','&','*','(',')',';','-','–','_','+','.', '?', '<', '>','/']
    
    stopwords = '''
        mais eu sob você a e i o u ou porém para não sim na no nas em nos portanto há esse essa esses essas 
        assim desta mas então os as do da de um uma sobre ser seja sem ter seu seus que com por das dos como
        cada ao aos muito muitos muita muitas às à é the in of ele ela nós nos eles elas and
        '''.split()

    sample = []

    for item in sample_raw:

        if item not in special_character + stopwords and not item.isnumeric() and len(item) > 1:

            sample.append(item)
    
    return sample


def count_words(sample):

    word = []

    frequency = []

    for unique in np.unique(sample):

        num_elements = len([x for x in sample if x == unique])

        word.append(unique)

        frequency.append(num_elements)

    freq_dict = {'word' : word, 'frequency' : frequency}

    return freq_dict


def count_phrases(list_of_words:list, words_in_phrase:int) -> dict:
    total_words = len(list_of_words)

    complete_phrase = ' '.join(list_of_words)

    ignore_phrase = []

    phrases = []

    counts = []

    for i in range(total_words - words_in_phrase):

        sub_phrase = ' '.join(list_of_words[i:i+3])

        if sub_phrase not in ignore_phrase:
            frequencies = complete_phrase.count(sub_phrase)

            phrases.append(sub_phrase)

            counts.append(frequencies)

            ignore_phrase.append(sub_phrase)

    return {'phrase' : phrases, 'frequency' : counts}


pdf_file = 'keywords-extractor\ementa.pdf'

sample_raw = extract_text_from_pdf(pdf_file = pdf_file)

sample = text_treatment(sample_raw = sample_raw)

# Word counting
words = count_words(sample = sample)
keywords = pd.DataFrame(words).sort_values(by='frequency', ascending=False).reset_index(drop=True)
keywords = keywords[keywords['frequency'] > 1]

# Phrase counting
phrases = count_phrases(list_of_words = sample, words_in_phrase = 3)
keyphrases = pd.DataFrame(phrases).sort_values(by='frequency', ascending=False).reset_index(drop=True)
keyphrases = keyphrases[keyphrases['frequency'] > 1]

# Saving dataframes as csv
keywords.to_csv('keywords-extractor\keywords.csv', index = False)
keyphrases.to_csv('keywords-extractor\keyphrases.csv', index = False)
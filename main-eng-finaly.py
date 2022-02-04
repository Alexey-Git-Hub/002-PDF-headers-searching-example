# -----------------------------------------------------------------------------
#  PDF file searching headers example
#
#  We need to find all headers which contained 'Balance sheet' and
#  return they number of pages.
#
#  Made by Alexey Loik
# -----------------------------------------------------------------------------

import io
import os

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import time
import fitz

INIT_FILENAME = 'config.init'
TEXT_TO_SEARCH = 'Balance Sheet'
MIN_POSITION = 0
MAX_POSITION = 100


def find_text_coord(filename, search_string, page_number):
    """
    Return list of y0 coordinates of searching text
        filename
        search_string
        page_number
    Return:
        coords_list  = list of coordinates search_string in PDF file page
    """

    coords_list = []

    with fitz.open(filename) as doc:
        page = doc[page_number]

        text = search_string
        text_instances = page.search_for(text)

        for inst in text_instances:
            coords_list.append(int(inst.y0))

    return coords_list


def extract_text_from_pdf(pdf_path, search_string):
    """
    Extract text from PDF file and creating list of founded strings
        pdf_path        = filename
        search_string   = searching text
    Return list of:
        page_no  = page number
        position = position if the searching text
        s_text   = original text of page
    """
    searching_text_origin = []

    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page_no, page in enumerate(PDFPage.get_pages(fh)):
            # print(page_no)
            page_interpreter.process_page(page)

            data = fake_file_handle.getvalue()
            data1 = data.lower()
            position = data1.find(search_string.lower())
            if position > -1:
                s_text = (data[position:(position + len(search_string))])
                searching_text_origin.append((page_no,
                                              position,
                                              s_text))
            fake_file_handle.truncate(0)
            fake_file_handle.seek(0)

    # close open handles
    converter.close()
    fake_file_handle.close()

    return searching_text_origin


def check_file(filename, find_string):
    """
    Checking PDF file for searching string enable. Printing to screen list of available pages.
        filename        = filename
        search_string   = searching text
    """
    start_time = time.time()
    searching_text_origin = extract_text_from_pdf(filename, find_string)

    new_list = []

    for s_item in searching_text_origin:
        y0 = find_text_coord(filename, find_string, page_number=s_item[0])
        for y in y0:
            new_list.append([s_item[0], s_item[2], y])

    end_time = time.time()
    pages = []

    for s_item in new_list:
        if s_item[2] <= MAX_POSITION and s_item[2] >= MIN_POSITION:
            pages.append([s_item[0], s_item[1], s_item[2]])
            print(f' Page: {s_item[0]+1}, Y0={s_item[2]}  Filename={filename}')

    print(f'-- Pages Count: {len(pages)}   ', end="")
    print(f'-- Total Repetitions: {len(searching_text_origin)}   ', end="")
    print("----- %s seconds ---" % (end_time - start_time))


def init_config(filename):
    """
    Reading from config file list of parameters.
        filename        = config filename
    """
    global MIN_POSITION
    global MAX_POSITION
    global TEXT_TO_SEARCH

    with open(filename, 'r') as file:
        for line in file:
            new_line = line.strip().split('=', 1)
            new_line_len = len(new_line)
            if new_line_len < 2:
                continue
            if new_line[0].lower() == 'min-pos':
               try:
                   MIN_POSITION = int(new_line[1])
               except Exception as Err:
                   print(f"Error: 'min-pos' invalid value. Default value={MIN_POSITION}")
            if new_line[0].lower() == 'max-pos':
               try:
                   MAX_POSITION = int(new_line[1])
               except Exception as Err:
                   print(f"Error: 'max-pos' invalid value. Default value={MAX_POSITION}")
            if new_line[0].lower() == 'text':
                TEXT_TO_SEARCH = new_line[1]
            # print(new_line_len, '  ', new_line)
    print(f'{MIN_POSITION=}')
    print(f'{MAX_POSITION=}')
    print(f'{TEXT_TO_SEARCH=}')


def run(search_string):
    """
    Reading the list of files to finding searched string.
    """
    dir_name = os.getcwd()

    for root, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".pdf"):
                print()
                print(f'Checking a PDF file {file} for pages with a search string')
                check_file(file, search_string)

if __name__ == '__main__':
    init_config(INIT_FILENAME)
    run(TEXT_TO_SEARCH)


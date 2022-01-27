import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

FILENAME = "C:\\Pycharm_projects\\venvs\\ve015_pdf_test\\MnM2019.pdf"

def extract_text_from_pdf(pdf_path):
    print('1')
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        pages = PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True)
        for x, page in enumerate(pages):
            page_interpreter.process_page(page)
            # print('-----------------------------------------')
            print(x)
            # print(page.contents)
            # print('-----------------------------------------')
            text2 = fake_file_handle.getvalue()
            # print(text2)
            if x==231:
                break;


        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


if __name__ == '__main__':
    text = extract_text_from_pdf(FILENAME)
    print(text[100:])
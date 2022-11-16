import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

import config
from utils import get_recipients


def replace_text(content: str, replacements: dict):
    lines = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result


def process_data(stream_object: EncodedStreamObject, replacements: dict):
    data = stream_object.getData()
    decoded_data = data.decode('utf-8')
    replaced_data = replace_text(decoded_data, replacements)
    encoded_data = replaced_data.encode('utf-8')

    if stream_object.decodedSelf is not None:
        stream_object.decodedSelf.setData(encoded_data)
    else:
        stream_object.setData(encoded_data)


def get_default_result_file_path(file_path: str):
    return file_path.replace(os.path.splitext(file_path)[1], "") + "_result"


def process_contents(contents, replacements):
    if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
        process_data(contents, replacements)
    elif contents is not None and len(contents) > 0:
        for obj in contents:
            if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                process_data(obj.getObject(), replacements)


def pdf_str_replace(file_path: str, replacements: dict, save_as: str = None):
    pdf = PdfFileReader(file_path)
    writer = PdfFileWriter()

    for page_number in range(0, pdf.getNumPages()):
        page = pdf.getPage(page_number)
        contents = page.getContents()

        process_contents(contents, replacements)

        # Force content replacement
        page[NameObject("/Contents")] = contents.decodedSelf
        writer.addPage(page)

    save_path = save_as if save_as else get_default_result_file_path(file_path)
    with open(save_path + ".pdf", 'wb') as out_file:
        writer.write(out_file)


def sanitize(string: str):
    return string.replace("ă", "a").replace("â", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")


if __name__ == '__main__':
    recipients = get_recipients(config.RECIPIENTS_LIST_FILE)

    contacts = {}
    for recipient in recipients:
        contacts.update(recipient)

    for email, name in contacts.items():
        print("Processing " + name + " <" + email + ">")
        result_directory = "attachments/" + email
        if not os.path.exists(result_directory):
            os.makedirs(result_directory, exist_ok=True)
        result_file = result_directory + "/Pre-Christmas Cocktail Party Invitation"
        pdf_str_replace('invitation.pdf', {'{{name}}': sanitize(name)}, result_file)

    print("Done!")

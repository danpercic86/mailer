import os.path

import yagmail

import config
from utils import get_recipients


def get_contents(file_path: str) -> str:
    with open(file_path, "r") as f:
        file_contents = f.read()

    if file_contents is None or file_contents == "":
        raise Exception(f"File {file_path} is empty!")

    return file_contents.replace("\n", "")


def get_attachments(emails: list[str]) -> list[str] | None:
    _attachments = ["attachments/" + email + "/Pre-Christmas Cocktail Party Invitation.pdf" for email in emails]

    for attachment in _attachments:
        if not os.path.isfile(attachment):
            print(f"!!!!!!!!! Attachment {attachment} not found! Skipping!")
            return None

    return _attachments


def send_email(receivers: dict[str, str]) -> None:
    emails = list(receivers.keys())

    print(f"Sending email to " + ", ".join([f"{name} <{email}>" for email, name in receivers.items()]))

    attachments = get_attachments(emails)
    if attachments is None:
        return

    names = list(receivers.values())
    if len(names) == 1:
        html = contents.replace("{{name}}", names[0])
    else:
        html = contents_plural.replace("{{name}}", ", ".join(names))

    yag.send(
        to=emails,
        subject=config.SUBJECT,
        contents=html,
        attachments=attachments,
    )

    print("Email sent!")


if __name__ == '__main__':
    yag = yagmail.SMTP({config.SENDER_EMAIL: config.SENDER_FULL_NAME}, config.SENDER_PASSWORD)
    contents = get_contents(config.BODY_HTML_FILE)
    filename, extension = config.BODY_HTML_FILE.rsplit(".", 1)
    contents_plural = get_contents(filename + '-plural.' + extension)

    for recipient in get_recipients(config.RECIPIENTS_LIST_FILE):
        send_email(recipient)

    print("All emails sent!")

from dotenv import dotenv_values

_config = dotenv_values("config.env")


def get_or_throw(variable: str):
    if value := _config.get(variable):
        return value

    raise Exception(f"Variable {variable} not found in config.env!")


SENDER_EMAIL = get_or_throw("SENDER_EMAIL")
SENDER_FULL_NAME = get_or_throw("SENDER_FULL_NAME")
SENDER_PASSWORD = get_or_throw("SENDER_PASSWORD")
BODY_HTML_FILE = get_or_throw("BODY_HTML_FILE")
SUBJECT = get_or_throw("SUBJECT")
RECIPIENTS_LIST_FILE = get_or_throw("RECIPIENTS_LIST_FILE")

ATTACHMENTS = _config.get("ATTACHMENTS").split(",") if _config.get("ATTACHMENTS") else None

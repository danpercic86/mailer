def get_recipients(file_path: str) -> list[dict[str, str]]:
    with open(file_path, "r") as f:
        recipients = f.read().splitlines()
        if len(recipients) == 0:
            raise Exception("No recipients provided!")

    result = []
    for recipient in recipients:
        if recipient == "":
            continue
        values = [receiver.split(",") for receiver in recipient.split(";")]
        result.append({value[0].strip(): value[1].strip() if value[1] else "" for value in values})

    return result


if __name__ == "__main__":
    print(get_recipients("recipients.txt"))

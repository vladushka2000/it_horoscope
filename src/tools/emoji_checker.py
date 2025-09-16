import emoji


def is_emoji(text: str) -> bool:
    if not text:
        return False

    text_without_emoji = emoji.replace_emoji(text, replace="")

    return text_without_emoji.strip() == ""

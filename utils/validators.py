import re


def is_valid_budget(text: str):
    text = text.replace(" ", "").replace(",", "")
    if text.isdigit():
        budget = int(text)
        if 50 <= budget <= 4000:
            return True, budget
    pattern = r'(\d+)\s*(?:$|dollars|dollar)?'
    match = re.match(pattern, text.lower())
    if match:
        number = int(match.group(1))
        budget = number
        if 50 <= budget <= 4000:
            return True, budget
    return False, None


def extract_budget_from_text(text: str):
    numbers = re.findall(r'\d+', text)

    for num_str in numbers:
        num = int(num_str)
        if 50 <= num <= 4000:
            return num
    return None

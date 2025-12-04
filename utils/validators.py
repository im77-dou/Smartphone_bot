import re


def is_valid_budget(text: str):
    if not text:
        return False, None
    text = text.strip().replace(" ", "").replace(",", "").replace("$", "")
    if not text:
        return False, None
    if len(text) > 15:
        return False, None
    if text.isdigit():
        budget = int(text)
        if 30 <= budget <= 4000:
            return True, budget
        return False, None

    pattern = r'^(\d+)\s*(?:USD|US|DOLLAR|DOLLARS)?$'
    match = re.match(pattern, text.lower())
    if match:
        try:
            number = int(match.group(1))
            if any(x in text.lower() for x in ["usd", "us", "dollar", "dollars"]):
                budget = number
            if 30 <= budget <= 4000:
                return True, budget
        except (ValueError, OverflowError):
            return False, None

    return False, None


def extract_budget_from_text(text: str):
    if not text or len(text) > 500:
        return None

    numbers = re.findall(r'\d+', text)
    if not numbers:
        return None

    for num_str in numbers:
        try:
            num = int(num_str)
            if 30 <= num <= 4000:
                return num
        except (ValueError, OverflowError):
            continue
    return None


def sanitize_text(text: str, max_length: int = 1000):
    if not text:
        return ""

    text = text[:max_length]
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')

    return text.strip()

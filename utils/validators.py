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


def is_valid_smartphone_name(text: str):
    if not text:
        return False, None, "Значение не может быть пустым"

    cleaned = text.strip()
    if not cleaned or cleaned.isspace():
        return False, None, "Значение не может быть пустым"

    if len(cleaned) < 2 or len(cleaned) > 50:
        return False, None, "Некорректное название смартфона"

    forbidden_chars = ['<', '>', '/', '\\', '{', '}', '[', ']', '|']
    for char in forbidden_chars:
        if char in cleaned:
            return False, None, "Некорректное название смартфона"

    if cleaned.isdigit():
        return False, None, "Некорректное название смартфона"

    return True, cleaned, None


def are_models_different(model1, model2):
    if not model1 or not model2:
        return False, "Одна из моделей не указана."

    normalized1 = " ".join(model1.split()).lower()
    normalized2 = " ".join(model2.split()).lower()

    if normalized1 == normalized2:
        return False, "Модели совпадают."

    return True, None


def validate_comparison_input(
        text,
        first_model: str | None = None
):
    is_valid, cleaned, error = is_valid_smartphone_name(text)

    if not is_valid:
        return {
            "is_valid": False,
            "cleaned_name": None,
            "error_message": error
        }

    if first_model:
        are_diff, diff_error = are_models_different(first_model, cleaned)
        if not are_diff:
            return {
                "is_valid": False,
                "cleaned_name": None,
                "error_message": diff_error
            }

    return {
        "is_valid": True,
        "cleaned_name": cleaned,
        "error_message": None
    }

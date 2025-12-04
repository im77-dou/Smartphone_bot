from typing import Any


def format_price(price: int | float):
    return f"{int(price):,}$".replace(",", " ")


def format_specs(specs: dict[str, Any]):
    lines = []
    spec_names = {
        "brand": "Бренд",
        "model": "Модель",
        "price": "Цена",
        "screen": "Экран",
        "soc": "Процессор",
        "ram": "Оперативная память",
        "rom": "Встроенная память",
        "battery": "Аккумулятор",
        "camera": "Камера"
    }
    for key, value in specs.items():
        if key in spec_names:
            name = spec_names[key]
            if key == "price" and isinstance(value, (int, float)):
                value = format_price(value)
            lines.append(f"{name}: <b>{value}</b>")
    return "\n".join(lines)


def truncate_text(
        text: str,
        max_length: int = 100,
        suffix: str = "..."
):
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_user_info(
        user_id: int,
        username: str | None,
        first_name: str
):
    username_str = f"@{username}" if username else ""
    return f"{first_name} {username_str} ({user_id})"

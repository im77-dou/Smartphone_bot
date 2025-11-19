import asyncio
import random


async def fetch_user_preferences(user_id):
    print(f"DB: Fetching preferences for user {user_id}...")
    await asyncio.sleep(random.uniform(0.5, 1.0))

    preferences = {
        "budget": random.choice([1000, 3000, 5000]),
        "brand": random.choice(["Apple", "Samsung", "Xiaomi"]),
        "camera": random.choice(["important", "unimportant"])
    }

    print(f"DB: Fetched preferences for user {user_id}: {preferences}")
    return preferences


async def ask_chatgpt(user_id, preferences, message):
    print(f"ChatGPT: Generating response for user {user_id}...")
    await asyncio.sleep(random.uniform(2.0, 3.0))

    response = f"ChatGPT: {message}"

    print(f"ChatGPT: Generated response for user {user_id}: {response}")
    return response


async def search_smartphone(preferences):
    print("Searching smartphones...")
    await asyncio.sleep(random.uniform(0.5, 1.0))

    smartphones = [
        {"model": "iPhone 17", "price": 3000},
        {"model": "Samsung Galaxy S25 Ultra", "price": 5000},
        {"model": "Xiaomi 15t", "price": 1000}
    ]

    filtered = [s for s in smartphones if s["price"] <= preferences["budget"]]

    print(f"Founded {len(filtered)} smartphones")
    return filtered


async def send_telegram_message(user_id, message):
    print(f"Telegram: Sending message to user {user_id}: {message}")
    await asyncio.sleep(random.uniform(0.2, 0.5))

    print(f"Telegram: Message sent to user {user_id}")


async def handle_user_request(user_id, message):
    print(f"\n{'='*60}")
    print(f"Request from user {user_id}: {message}")
    print(f"{'='*60}\n")

    preferences = await fetch_user_preferences(user_id)
    gpt_response = await ask_chatgpt(user_id, preferences, message)
    smartphones = await search_smartphone(preferences)

    final_message = f"{gpt_response}\n\nAvailable smartphones:\n"
    for smartphone in smartphones:
        final_message += f"- {smartphone['model']}: (${smartphone['price']})\n"

    await send_telegram_message(user_id, final_message)

    print(f"Request handled for user {user_id}")


async def main():
    print("Bot is running...\n")

    await asyncio.gather(
        handle_user_request(1, "I want to buy a smartphone"),
        handle_user_request(2, "I need smartphone with a good camera"),
        handle_user_request(3, "Whos better, iPhone or Samsung?")
    )

    print("\nRequest handling completed.")


if __name__ == "__main__":
    import time

    start = time.time()
    asyncio.run(main())
    end = time.time()

    print(f"\n{'='*60}")
    print(f"Execution time 3 users: {end - start:.2f} seconds")
    print(f"{'='*60}")

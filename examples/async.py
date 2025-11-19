import asyncio


async def greet_user(name):
    print(f"Started greeting user {name}")
    await asyncio.sleep(1)
    greeting = f"Hello {name}"
    print(f"Finished greeting user {name}")
    return greeting


async def main():
    print("=== Example 1: Sequential execution ===\n")

    result_1 = await greet_user("Alex")
    print(f"Result 1: {result_1}\n")

    result_2 = await greet_user("Mary")
    print(f"Result 2: {result_2}\n")

    result_3 = await greet_user("John")
    print(f"Result 3: {result_3}\n")


if __name__ == "__main__":
    import time

    start = time.time()

    asyncio.run(main())

    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
    print(f"Waiting time: {end - start - 3}")

import asyncio

from autocomeback.__main__ import main as autocomeback


def main(event, context):
    results = asyncio.run(autocomeback())
    print(f"{results} ok")

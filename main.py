import asyncio

from autocomeback import autocomeback


def main(event, context):
    results = asyncio.run(autocomeback())
    print(f"{results} ok")

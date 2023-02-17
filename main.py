import asyncio

from flask import Request

from autocomeback import autocomeback


def main(request: Request):
    results = asyncio.run(autocomeback(cloud=True))
    return f"{results} ok"

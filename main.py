import asyncio

from flask import Request

from autocomeback import autocomeback


def main(request: Request):
    results = asyncio.run(autocomeback())
    return f"{results} ok"

from flask import Request

from autocomeback import autocomeback


def main(request: Request):
    results = autocomeback()
    return f"{results} ok"

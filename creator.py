#!/usr/bin/python3

import argparse
import os
from textwrap import dedent
from time import sleep

from animesource_scaffolder import AnimeSourceScaffolder
from mangasource_scaffolder import MangaSourceScaffolder

def specific_choice(text: str, valid: list[int] = [1, 2]) -> int:
    while True:
        response = input(dedent(text))
        print()

        if not response.isnumeric():
            print("Invalid choice: Enter numbers only!")
        else:
            choice = int(response)
            if choice in valid:
                return choice
            else:
                print("Invalid choice!")

        sleep(1)
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-a", "--anime", action="store_true", help="Creates a anime extension. Takes precedence over --manga.")
    args.add_argument("-m", "--manga", action="store_true", help="Creates a manga extension.")
    args.add_argument("-n", "--name", action="store", help="Name of the source")
    args.add_argument("-l", "--lang", action="store", help="Language of the source")
    args.add_argument("-b", "--base-url", action="store", help="Base URL of the source")
    args.add_argument(
        "-p",
        "--parsed",
        action=argparse.BooleanOptionalAction,
        help="Use ParsedHttpSource as base to the main class"
    )
    values = args.parse_args()
    is_manga = values.manga and not values.anime
    if not (values.anime or values.manga):
        is_manga = specific_choice("""
            Choose the extension type:
                1. Anime extension / Aniyomi
                2. Manga extension / Tachiyomi

            Enter your choice: """) == 2

    name = values.name or input("Source name: ")
    lang = values.lang or input("Source language: ")
    baseUrl = values.base_url or input("Base URL: ")
    is_parsed = values.parsed

    if is_parsed is None:
        is_parsed = specific_choice("""
            Choose the base class:
                1. HttpSource / API/JSON oriented
                2. ParsedHttpSource / JSoup/CSS oriented

            Enter your choice: """) == 2
     

    args = (is_parsed, name, lang, baseUrl)
    scaffold = MangaSourceScaffolder(*args) if is_manga else AnimeSourceScaffolder(*args)
    scaffold.create_dirs()
    scaffold.create_files()

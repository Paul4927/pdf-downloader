"""
File: pdf_downloader.py
Author: Paul Kenneth Fortaleza
Email: paulkennethfortaleza@gmail.com
Date: 2024-09-17
Description: This script was made to help a friend easily look for pdf materials
            online instead of browsing the internet manually
"""
import os
from pathlib import Path
from googlesearch import search
import requests
import const

results = []
links = []
output_path = os.path.join(Path.cwd(), const.DOWNLOAD_FOLDER)
i = const.RESULT_INDEX


def _clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


try:
    user_input = input(const.PROMPT_SEARCH)
    query = f"{user_input}:{const.QUERY_FILE_TYPE}"

    for url in search(query):
        if const.OUTPUT_EXTENSION in url:
            results.append(url)
        else:
            links.append(url)

    if results:
        print(const.PROMPT_SELECT_LINK)

        for result in results:
            print(f"\t{i}. {result}")
            i += 1

        while True:
            try:
                selected_index = int(input(const.PROMPT_SELECT_NUM))
                if 0 < selected_index <= len(results):
                    break
                print(const.MSG_INVALID_NUM)
            except ValueError:
                print(const.MSG_NOT_NUM)

        selected_link = results[selected_index - 1]

        _clear_screen()
        print(const.MSG_DOWNLOADING)
        response = requests.get(selected_link, timeout=const.REQUEST_TIMEOUT)

        if response.status_code == const.SUCCESS_CODE:
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            with open(
                os.path.join(output_path, f"{user_input}.{const.QUERY_FILE_TYPE}"),
                "wb"
            ) as pdf_file:
                pdf_file.write(response.content)
            _clear_screen()
            print(const.MSG_EXECUTION_SUCCESS)
            input(const.MSG_EXIT)
        else:
            _clear_screen()
            input(f"{const.MSG_DOWNLOAD_ERROR}{const.MSG_EXIT}")
    elif links:
        _clear_screen()
        print(const.MSG_NO_RESULT, const.MSG_LINKS_RESULT)
        for link in links:
            print(f"\t{i}. {link}")
            i += 1
        input(const.MSG_EXIT)
    else:
        _clear_screen()
        input(f"{const.MSG_NO_RESULT}\n{const.MSG_EXIT}")

except Exception as e:  # pylint: disable=broad-except
    _clear_screen()
    print(const.MSG_EXCEPTION % (e, const.MSG_EXIT))

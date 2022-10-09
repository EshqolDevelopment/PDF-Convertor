import os
import threading
import time

from kivy.clock import mainthread
from kivymd.uix.button import MDFlatButton
from pdf2docx import Converter
import fitz


def convert_pdf_to_docs(pdf_path: str, word_path: str):
    cv = Converter(pdf_path)
    cv.convert(word_path)
    cv.close()
    return word_path


def pdf_to_text(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def pdf_to_html_st(pdf_path):
    doc_ok = fitz.open(pdf_path)

    html_text = ''
    for page in doc_ok:
        html_text += page.get_text("html")
    return html_text


def pdf_to_html(pdf_path: str, html_path: str):
    text = pdf_to_html_st(pdf_path)

    with open(html_path, 'wb') as f:
        f.write(text.encode())


def pdf_to_txt(pdf_path: str, txt_path: str):
    text = pdf_to_text(pdf_path)

    with open(txt_path, 'wb') as f:
        f.write(text.encode())


def img_to_pdf(pdf_path: str, dir_path: str):
    doc = fitz.open(pdf_path)

    i = 1
    for page in doc:
        pix = page.get_pixmap()
        pix.save(f"{dir_path}/page_{i}.png")
        i += 1


def convert_hic(pdf_path, convert_path, kind, snack):
    tic = time.perf_counter()
    try:
        if kind == "html":
            pdf_to_html(pdf_path, convert_path)
        elif kind == "img":
            img_to_pdf(pdf_path, convert_path)
        elif kind == "txt":
            pdf_to_txt(pdf_path, convert_path)
        elif kind == "word":
            convert_pdf_to_docs(pdf_path, convert_path)

        change_snack(snack, convert_path, time.perf_counter() - tic)

    except Exception:
        change_snack_error(snack, time.perf_counter() - tic)


@mainthread
def change_snack_error(snack, tic):
    snack.text = "An unexpected error accrued"
    snack.duration = tic + 5


@mainthread
def change_snack(snack, convert_path, tic):
    snack.text = "The file was converted successfully"

    snack.buttons = [
        MDFlatButton(
            text="[color=#1aaaba]OPEN[/color]",
            on_release=lambda x: threading.Thread(target=lambda: os.startfile(convert_path), daemon=True).start(),
        ),
    ]
    snack.duration = tic + 8



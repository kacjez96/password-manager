import flet as ft
from controller import Controller

def main(page: ft.Page):
    # Run
    Controller(page)

ft.app(target=main)

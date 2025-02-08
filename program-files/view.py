import time
import gc
from abc import ABC, abstractmethod
import flet as ft
from flet import colors

gc.collect()


class View(ABC):
    @abstractmethod
    def __init__(self, controller):
        self.controller = controller

    def build(self, page: ft.Page):
        # Page Settings
        self.page = page
        # self.page.window_maximized = True
        self.page.window_center()
        self.page.title = "Menadżer Haseł"
        self.page.theme_mode = ft.ThemeMode.DARK


# Start View
class SignIn(View):
    def __init__(self, controller):
        super().__init__(controller)
        self.haslo = ft.TextField(
            label="Hasło",
            password=True,
            can_reveal_password=True,
            filled=True,
            text_size=35,
            border_radius=20,
            hint_text="Podaj hasło",
            label_style=ft.TextStyle(size=20),
            on_submit=self.controller.logging,
        )

    def build(self, page: ft.Page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        start = ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        width=500,
                        controls=[
                            ft.Container(
                                content=self.haslo,
                                alignment=ft.alignment.center,
                            ),
                        ]
                    )
                )
            ]
        )

        self.page.add(start)

    def banner_logged(self):
        logged = ft.Banner(
            divider_color=colors.BACKGROUND,
            content=ft.Text(
                "ZALOGOWANO",
                text_align=ft.TextAlign.CENTER,
                size=30,
                color=colors.GREEN,
                weight=ft.FontWeight.BOLD,
            ),
            actions=[
                ft.Text("", color=colors.BACKGROUND)
            ]
        )
        self.page.banner = logged
        logged.open = True
        self.page.update()
        logged.open = False
        time.sleep(4)
        self.page.close_banner()
        time.sleep(1 / 10)

    def banner_wrong(self):
        wrong = ft.Banner(
            divider_color=colors.BACKGROUND,
            content=ft.Text(
                "BŁĘDNE HASŁO",
                text_align=ft.TextAlign.CENTER,
                size=30,
                color=colors.RED,
                weight=ft.FontWeight.BOLD,
            ),
            actions=[
                ft.Text("", color=colors.BACKGROUND)
            ]
        )
        self.page.banner = wrong
        wrong.open = True
        self.page.update()
        time.sleep(3)
        self.page.close_banner()
        self.page.update()


class MainView(View):
    def __init__(self, controller):
        super().__init__(controller)
        self.title_field = ft.TextField(
            label="Tytuł",
            on_submit=self.controller.add_password,
            col={"xl": 10}
        )
        self.login_field = ft.TextField(
            label="Login",
            on_submit=self.controller.add_password,
            col={"xl": 5}
        )
        self.password_field = ft.TextField(
            label="Hasło",
            on_submit=self.controller.add_password,
            col={"xl": 5},
        )
        self.panel = ft.ExpansionPanelList(
            divider_color=colors.AMBER_700,
            col={"xl": 11},
        )

    def build(self, page: ft.Page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        switch_theme = ft.Switch(
            on_change=self.controller.change_theme,
            height=50
        )

        add_pass_fields = ft.Column(
            [
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            ft.Text(
                                "DODAJ HASŁO",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=colors.CYAN,
                            ),
                            col={"xl": 10},
                            alignment=ft.alignment.center,
                            margin=10
                        ),
                        ft.Container(
                            content=switch_theme,
                            col={"xl": 2},
                            alignment=ft.alignment.center_right,
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    [
                        self.title_field
                    ],
                ),
                ft.ResponsiveRow(
                    [
                        self.login_field,
                        self.password_field,
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Text(
                                    "Dodaj",
                                    size=25,
                                    text_align=ft.alignment.center,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                color=colors.DEEP_PURPLE_900,
                                bgcolor=colors.BLUE_400,
                                height=55,
                                width=150,
                                on_click=self.controller.add_password,
                            ),
                            col={"xl": 2},
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.alignment.center
                ),
            ],
        )

        self.page.add(add_pass_fields)

        password_list = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.ResponsiveRow(
                    [
                        self.panel,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )

        database = ft.Column(
            [
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            ft.Text(
                                "BAZA HASEŁ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=colors.DEEP_ORANGE_800,
                            ),
                            col={"xl": 3},
                            alignment=ft.alignment.center,
                            margin=20
                        )
                    ],
                ),
                ft.ResponsiveRow(
                    [
                        password_list,
                    ],
                    expand=1
                )
            ],
            expand=True,
        )
        self.page.add(database)

    def update_password_list(self, passwords):
        self.panel.controls.clear()

        for index, entry in enumerate(passwords):
            self.panel.controls.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(
                        title=ft.Text(
                            f"{entry['title']}",
                            size=23,
                            weight=ft.FontWeight.BOLD,
                        ),
                        trailing=ft.IconButton(
                            ft.icons.DELETE,
                            on_click=lambda e, i=index: self.controller.delete_password(i)
                        )
                    ),
                    can_tap_header=True,
                    content=ft.ListTile(
                        title=ft.Text(f"Login: {entry['login']}\nHasło: {entry['password']}"),
                        leading=ft.IconButton(
                            ft.icons.VISIBILITY_OFF,
                            on_click=lambda e, i=index: self.controller.show_hide_password(i, passwords[i]),
                        ),
                    ),
                )
            )
        self.page.update()

    def show_hide_password(self, index, entry):
        self.panel.controls[index].content.title.value = f"Login: {entry['login']}\nHasło: {entry['password']}"
        if self.panel.controls[index].content.leading.icon == ft.icons.VISIBILITY_OFF:
            self.panel.controls[index].content.leading.icon = ft.icons.VISIBILITY
        else:
            self.panel.controls[index].content.leading.icon = ft.icons.VISIBILITY_OFF
        self.page.update()

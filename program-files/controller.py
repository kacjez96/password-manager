import flet as ft
from model import Model
from view import SignIn, MainView


# Controller
class Controller:
    def __init__(self, page: ft.Page):
        self.model = Model()
        self.login_view = SignIn(self)
        self.manager_view = MainView(self)
        self.login_view.build(page)

    def logging(self, e=None):
        hashed = self.model.hash(self.login_view.haslo.value)
        pass_secret = self.model.pass_secret
        if hashed == pass_secret:
            self.login_view.banner_logged()
            self.login_view.page.clean()
            self.new_page()
            self.model.set_key(self.login_view.haslo.value)
        else:
            self.login_view.banner_wrong()

    def new_page(self, e=None):
        self.manager_view.build(self.login_view.page)
        self.manager_view.update_password_list(self.model.get_passwords())
        self.manager_view.page.update()
        print(f"Obecne zahashowane hasło: {self.model.__str__()}")
        print(f"Ilość haseł w bazie danych: {self.model.__len__()}")

    def change_theme(self, e=None):
        self.manager_view.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.manager_view.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.manager_view.page.update()

    def add_password(self, e=None):
        title = self.manager_view.title_field.value
        login = self.manager_view.login_field.value
        password = self.manager_view.password_field.value
        if title and login and password:
            self.model.add_password(title, login, password)
            self.manager_view.update_password_list(self.model.get_passwords())
            self.manager_view.title_field.value = ""
            self.manager_view.login_field.value = ""
            self.manager_view.password_field.value = ""
            print(f"Ilość haseł w bazie danych: {self.model.__len__()}")
            self.manager_view.page.update()

    def delete_password(self, index):
        self.model.delete_password(index)
        print(f"Ilość haseł w bazie danych: {self.model.__len__()}")
        self.manager_view.update_password_list(self.model.get_passwords())

    def show_hide_password(self, index, password):
        self.model.show_hide_password(index)
        self.manager_view.show_hide_password(index, password)

import json
import flet as ft

link_discord = "https://discord.gg/vcQMwRzbak"

news = [
    (
        """
Version 1.0.0,
Add: News system
https://discord.gg/vcQMwRzbak 🤓
""",
        "11/06/2022",
    ),
    ("Oasis 1.0.0.0", "12/06/2022"),
    (
        """
Version 1.0.0,
Add: News system
https://discord.gg/vcQMwRzbak 🤓
""",
        "11/06/2022",
    ),
    ("Oasis 1.0.0.0", "12/06/2022"),
    (
        """
Version 1.0.0,
Add: News system
https://discord.gg/vcQMwRzbak 🤓
""",
        "11/06/2022",
    ),
    ("Oasis 1.0.0.0", "12/06/2022"),
]


def open_url(url):
    def _open_url(e):
        e.page.launch_url(url)

    return _open_url


def create_new(text, fecha):
    return ft.Container(
        content=ft.Column(
            [ft.Text(fecha, size=12), ft.Text(text)],
        ),
        bgcolor="#9eaab6",
        border_radius=12,
        padding=ft.padding.all(10),
        width=700,
    )


def load_config(file):
    with open(file, "r") as i:
        config = json.load(i)
    return config


def main(page: ft.Page):
    page.title = "Oasis Client"  # Nombre del cliente
    page.window_always_on_top = True
    page.bgcolor = "#1A1C1E"

    # Botón de jugar
    play_button = ft.FilledButton("JUGAR")

    # Imagen principal
    image = ft.Container(
        content=ft.Image("assets/image.png", fit=ft.ImageFit.SCALE_DOWN),
        height=500,
        width=700,
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.only(left=60),
    )

    # Botones de configuración, Discord y Home
    settings_button = ft.Container(
        content=ft.IconButton(
            ft.icons.SETTINGS, icon_color="white", width=50, height=50
        ),
        alignment=ft.alignment.top_center,
    )

    discord_button = ft.Container(
        content=ft.IconButton(
            ft.icons.DISCORD,
            icon_color="white",
            width=50,
            height=50,
            on_click=open_url(link_discord),
        ),
        alignment=ft.alignment.top_center,
    )

    home_button = ft.Container(
        content=ft.IconButton(ft.icons.HOME, icon_color="white", width=50, height=50),
        alignment=ft.alignment.top_center,
    )

    # Añadiendo todos los componentes a la página
    page.add(
        ft.Column(
            [
                ft.Container(
                    ft.Row(
                        [settings_button, image, discord_button, home_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    height=210,
                ),
                ft.Container(
                    content=ft.Row(
                        [ft.TextButton("NEW's"), ft.TextButton("UPDATE's")],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Column(
                        [create_new(i, e) for i, e in news],
                        scroll=ft.ScrollMode.HIDDEN,
                    ),
                    bgcolor="red",
                    padding=ft.padding.all(27),
                    alignment=ft.alignment.center,
                    height=400,
                ),
                ft.Container(
                    content=play_button,
                ),
            ],
            spacing=10,
        )
    )


ft.app(target=main)

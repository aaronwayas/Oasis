import flet as ft
import minecraft_launcher_lib as mclib

import json
import os
import subprocess


minecraft_dir = os.getenv("APPDATA") + "\\.minecraftLauncher"

versions_vanilla = [
    version["id"]
    for version in mclib.utils.get_version_list()
    if version["type"] == "release"
]

link_discord = "https://discord.gg/vcQMwRzbak"


def load_news_updates():
    try:
        with open("utils/news_updates.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File 'news_updates.json' not found")
        return {"news": [], "updates": []}
    except json.JSONDecodeError:
        print("File 'news_updates.json' is not valid JSON")
        return {"news": [], "updates": []}


news_updates = load_news_updates()

news = news_updates.get("news", [])
updates = news_updates.get("updates", [])


def install_version(page: ft.Page, version: str):
    if get_install_status(version) == "Installed":
        print(f"Version {version} is already installed")
        return

    try:
        print(f"Installing version {version}")
        mclib.install.install_minecraft_version(version, minecraft_dir)
        create_dialog(page, "Success", f"Version {version} installed successfully")
    except Exception as e:
        print(f"Error installing version {version}: {e}")
        create_dialog(page, "Error", f"Error installing version {version}: {e}")


def load_config():
    try:
        with open("utils/config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found")
        return {"username": "", "ram": 1}
    except json.JSONDecodeError:
        print("Config file is not valid JSON")
        return {"username": "", "ram": 1}
    except TypeError:
        return {"username": "", "ram": 1}


def create_dialog(page: ft.Page, title: str, content: str):
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        open=True,
    )
    page.dialog = dialog
    page.update()


def save_config(page: ft.Page, path, username: str, ram: str):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    if not username or not ram:
        create_dialog(page, "Error", "Username or RAM value is empty")
        return

    try:
        ram_float = float(ram)
        ram = (
            str(int(ram_float)) if ram_float.is_integer() else str(round(ram_float, 1))
        )
        with open(path, "w") as f:
            json.dump({"username": username, "ram": ram}, f)
        create_dialog(page, "Config saved!", "Config saved successfully!")
    except Exception as e:
        create_dialog(page, "Error", f"Error saving config: {e}")


def create_news_item(item):
    text = item.get("text", "No text available")
    fecha = item.get("date", "No date available")

    return ft.Container(
        content=ft.Column(
            [ft.Text(fecha, size=12, color="black"), ft.Text(text, color="black")],
        ),
        bgcolor="#9eaab6",
        border_radius=12,
        padding=ft.padding.all(10),
        width=700,
    )


def get_date_version(version):
    for ver in mclib.utils.get_version_list():
        if ver["id"] == version:
            release_time = ver["releaseTime"]
            return str(release_time)[:16]
    return None


def get_type_version(version):
    for ver in mclib.utils.get_version_list():
        if ver["id"] == version:
            return ver["type"]
    return None


def get_install_status(version):
    for ver in mclib.utils.get_installed_versions(minecraft_dir):
        if ver["id"] == version:
            return "Installed"
    return "Not Installed"


def run_minecraft(username, ram, version):
    try:
        options = {
            "username": username,
            "uuid": "",
            "token": "",
            "launcherVersion": "0.0.2",
        }
        options["jvmArguments"] = [f"-Xmx{ram}G", f"-Xms{ram}G"]
        minecraft_command = mclib.command.get_minecraft_command(
            version, minecraft_dir, options
        )
        subprocess.run(minecraft_command)
    except Exception as e:
        print(f"Error running Minecraft: {e}")


def main(page: ft.Page):
    page.title = "Oasis Client"
    page.window_always_on_top = False  # off on release
    page.bgcolor = "#1A1C1E"

    def go_to_home(version: str):
        version_button.content.value = version
        play_button.on_click = lambda _: run_minecraft(
            load_config()["username"], load_config()["ram"], version
        )
        page.go("/")

    def show_version_details(version: str):
        version_details.content.alignment = ft.MainAxisAlignment.START
        version_details.content.horizontal_alignment = ft.CrossAxisAlignment.START

        version_details.content.controls = [
            ft.Text(f"Version {version}", size=30, weight=ft.FontWeight.BOLD),
            ft.Text(f"Date: {get_date_version(version)}", size=20),
            ft.Text(
                f"Type: {get_type_version(version)} Status: {get_install_status(version)}",
                size=20,
            ),
            ft.Row(
                [
                    ft.ElevatedButton("Select", on_click=lambda _: go_to_home(version)),
                    ft.ElevatedButton(
                        "Download", on_click=lambda _: install_version(page, version)
                    ),
                ]
            ),
        ]
        page.update()

    def create_version_item(version: str):
        return ft.Container(
            content=ft.Column(
                [ft.Text(version, size=30)],
            ),
            padding=ft.padding.all(10),
            border_radius=12,
            height=70,
            width=250,
            bgcolor="#242a30",
            on_click=lambda _: show_version_details(version),
        )

    version_details = ft.Container(
        content=ft.Column(
            [ft.Text("Select a version", size=30, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#2d3740",
        border_radius=12,
        expand=True,
        padding=10,
    )

    version_button = ft.FilledButton(
        content=ft.Text("VERSION", color="white", size=17),
        style=ft.ButtonStyle(
            bgcolor="#607885", shape=ft.RoundedRectangleBorder(radius=10)
        ),
        width=150,
        height=45,
        on_click=lambda e: page.go("/download"),
    )

    play_button = ft.FilledButton(
        content=ft.Text("JUGAR", color="white", size=17),
        style=ft.ButtonStyle(
            bgcolor="#59C4FF", shape=ft.RoundedRectangleBorder(radius=15)
        ),
        width=150,
        height=45,
        on_click=lambda _: create_dialog(
            page,
            "Select a version",
            "Select a version first to play (In the versions view)",
        ),
    )

    image = ft.Container(
        content=ft.Image("assets/image.png", fit=ft.ImageFit.SCALE_DOWN),
        height=500,
        width=700,
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.only(left=60),
    )

    news_container = ft.Container(
        content=ft.Column(
            [create_news_item(x) for x in news],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.alignment.top_center,
        height=400,
        expand=True,
    )

    def show_news(e, news_btn, updates_btn):
        news_container.content.controls = [create_news_item(x) for x in news]
        news_btn.style.bgcolor = "#242a30"
        updates_btn.style.bgcolor = ft.colors.TRANSPARENT
        page.update()

    def show_updates(e, news_btn, updates_btn):
        news_container.content.controls = [create_news_item(x) for x in updates]
        news_btn.style.bgcolor = ft.colors.TRANSPARENT
        updates_btn.style.bgcolor = "#242a30"
        page.update()

    news_button_style = ft.ButtonStyle(
        bgcolor=ft.colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    updates_button_style = ft.ButtonStyle(
        bgcolor=ft.colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    news_button = ft.TextButton(
        "NEW's",
        style=news_button_style,
        on_click=lambda e: show_news(e, news_button, updates_button),
    )

    updates_button = ft.TextButton(
        "UPDATE's",
        style=updates_button_style,
        on_click=lambda e: show_updates(e, news_button, updates_button),
    )

    bar_container = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    ft.icons.SETTINGS,
                    icon_color="white",
                    width=50,
                    height=50,
                    on_click=lambda e: page.go("/settings"),
                ),
                image,
                ft.IconButton(
                    ft.icons.DISCORD,
                    icon_color="white",
                    width=50,
                    height=50,
                    url=link_discord,
                ),
                ft.IconButton(
                    ft.icons.HOME,
                    icon_color="white",
                    width=50,
                    height=50,
                    on_click=lambda e: page.go("/"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        height=200,
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                bar_container,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        news_button,
                                        updates_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),
                            news_container,
                        ],
                        height=400,
                    ),
                    padding=ft.padding.all(10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            version_button,
                            play_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    height=55,
                    bgcolor="#141618",
                    padding=ft.padding.only(right=10, left=10),
                    border_radius=ft.border_radius.all(20),
                ),
            ],
            spacing=1,
        ),
        expand=True,
    )

    def update_ram(e):
        print(e.control.value)

    username_field = ft.TextField(
        value=load_config()["username"],
        border_color="white",
        border_width=0.5,
        border_radius=ft.border_radius.all(10),
        height=50,
    )

    ram_slider = ft.Slider(
        min=0,
        max=16,
        divisions=16,
        value=1,
        on_change=update_ram,
        label="{value} GB",
    )

    save_button = ft.FilledButton(
        content=ft.Text("SAVE", color="white", size=17),
        style=ft.ButtonStyle(
            bgcolor="#59C4FF", shape=ft.RoundedRectangleBorder(radius=15)
        ),
        width=150,
        height=45,
        on_click=lambda e: save_config(
            page, "utils/config.json", username_field.value, ram_slider.value
        ),
    )

    config_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Username"),
                                    username_field,
                                ]
                            ),
                            bgcolor="#2d3740",
                            padding=ft.padding.all(10),
                            border_radius=ft.border_radius.all(10),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("RAM"),
                                    ram_slider,
                                ]
                            ),
                            bgcolor="#2d3740",
                            padding=ft.padding.all(10),
                            border_radius=ft.border_radius.all(10),
                            expand=True,
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Oasis Client: 1.0.1"),
                                    ft.Text("Programado por:\nDiseñado por:"),
                                ]
                            ),
                            bgcolor="#2d3740",
                            padding=ft.padding.all(10),
                            border_radius=ft.border_radius.all(10),
                            expand=True,
                        )
                    ]
                ),
            ]
        ),
        expand=True,
    )

    def get_vanilla_versions():
        return [
            version["id"]
            for version in mclib.utils.get_version_list()
            if version["type"] == "release"
        ]

    def get_forge_versions(max: int = 50):
        versions = mclib.forge.list_forge_versions()
        versions = versions[:max]

        return versions

    def get_installed_versions():
        return [
            version["id"]
            for version in mclib.utils.get_installed_versions(minecraft_dir)
        ]

    def update_versions_list(e, category):
        if category == "Vanilla":
            versions = get_vanilla_versions()
        elif category == "Forge":
            versions = get_forge_versions(50)
        else:  # Others
            versions = get_installed_versions()

        items_version.controls = [create_version_item(version) for version in versions]
        page.update()

    vanilla_button = ft.Container(
        ft.Text("Vanilla", size=20, color="white"),
        bgcolor="#242a30",
        expand=True,
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=lambda e: update_versions_list(e, "Vanilla"),
    )

    forge_button = ft.Container(
        ft.Text("Forge", size=20, color="white"),
        bgcolor="#242a30",
        expand=True,
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=lambda e: update_versions_list(e, "Forge"),
    )

    others_button = ft.Container(
        ft.Text("Others", size=20, color="white"),
        bgcolor="#242a30",
        expand=True,
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=lambda e: update_versions_list(e, "Others"),
    )

    items_version = ft.Column(
        [create_version_item(version) for version in versions_vanilla],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    versions_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [vanilla_button, forge_button, others_button],
                    ),
                    height=50,
                ),
                ft.Row(
                    [
                        ft.Column([items_version]),
                        version_details,
                    ],
                    spacing=20,
                    expand=True,
                ),
            ],
        ),
        expand=True,
    )

    def route_change(route):
        if page.route == "/":
            page.views.clear()
            page.views.append(ft.View("/", [main_container]))
        elif page.route == "/download":
            page.views.append(
                ft.View(
                    "/download",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    bar_container,
                                    versions_container,
                                ],
                            ),
                            expand=True,
                        )
                    ],
                )
            )
        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    bar_container,
                                    config_container,
                                    ft.Container(
                                        content=ft.Row(
                                            [save_button],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                        height=55,
                                        bgcolor="#141618",
                                        padding=ft.padding.only(right=10, left=10),
                                        border_radius=ft.border_radius.all(20),
                                    ),
                                ]
                            ),
                            expand=True,
                        )
                    ],
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/404",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("404", size=40),
                                    ft.Text("Page not found", size=20),
                                    ft.ElevatedButton(
                                        "Go Home", on_click=lambda _: page.go("/")
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            expand=True,
                            alignment=ft.alignment.center,
                        )
                    ],
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")


ft.app(target=main)

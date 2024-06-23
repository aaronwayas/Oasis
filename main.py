import flet as ft

link_discord = "https://discord.gg/vcQMwRzbak"

news = [
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
    ("Version 1.0.0, Add: News system", "11/06/2022"),
]

updates = [
    ("Version 1.1.0, Update: Bug fixes", "12/07/2022"),
    ("Version 1.1.0, Update: Performance improvements", "12/07/2022"),
    ("Version 1.1.0, Update: New feature added", "12/07/2022"),
    ("Version 1.1.0, Update: UI improvements", "12/07/2022"),
]


def create_new(text, fecha):
    return ft.Container(
        content=ft.Column(
            [ft.Text(fecha, size=12, color="black"), ft.Text(text, color="black")],
        ),
        bgcolor="#9eaab6",
        border_radius=12,
        padding=ft.padding.all(10),
        width=700,
    )


def main(page: ft.Page):
    page.title = "Oasis Client"  # Nombre del cliente
    page.window_always_on_top = True
    page.bgcolor = "#1A1C1E"

    version_button = ft.FilledButton(
        content=ft.Text("VERSION", color="white", size=17),
        style=ft.ButtonStyle(
            bgcolor="#607885", shape=ft.RoundedRectangleBorder(radius=10)
        ),
        width=150,
        height=45,
    )
    play_button = ft.FilledButton(
        content=ft.Text("JUGAR", color="white", size=17),
        style=ft.ButtonStyle(
            bgcolor="#59C4FF", shape=ft.RoundedRectangleBorder(radius=15)
        ),
        width=150,
        height=45,
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
            [create_new(x[0], x[1]) for x in news],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            height=400,  # Adjust the height as needed
        ),
        alignment=ft.alignment.center,
        height=400,  # Adjust the height as needed
    )

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

    def show_news(e, news_btn, updates_btn):
        news_container.content.controls = [create_new(x[0], x[1]) for x in news]
        news_btn.style.bgcolor = "#242a30"
        updates_btn.style.bgcolor = ft.colors.TRANSPARENT
        page.update()

    def show_updates(e, news_btn, updates_btn):
        news_container.content.controls = [create_new(x[0], x[1]) for x in updates]
        news_btn.style.bgcolor = ft.colors.TRANSPARENT
        updates_btn.style.bgcolor = "#242a30"
        page.update()

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
                        alignment=ft.MainAxisAlignment.CENTER,
                        height=400,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10),
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
        padding=ft.padding.all(1),
        expand=True,
        alignment=ft.alignment.center,
    )

    def route_change(route):
        if page.route == "/":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [main_container],
                )
            )
        elif page.route == "/download":
            page.views.append(
                ft.View(
                    "/download",
                    [],
                )
            )

        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [bar_container],
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

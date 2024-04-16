import flet as ft
import os

dir_list = ""
dir_name = ""
image_no = 0

def main(page: ft.Page):

    #FUNCTIONS-------------------------
    def change_dir(e):
        global dir_list, dir_name

        dir_name = dir_textfield.value
        dir_list = os.listdir(dir_name)

        #Filter the dir for images only
        filter_dir_for_images()

        image_section.src = os.path.join(dir_name, dir_list[0])
        image_section.update()
        get_caption(e)

    def filter_dir_for_images():
        global dir_list

        temp_list = []

        for file in dir_list:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                temp_list.append(file)

        dir_list = temp_list
        dir_list = sorted(dir_list)

    #view diff images
    def change_image_right(e):
        global image_no

        if image_no < len(dir_list)-1:
            image_no = image_no + 1
            image_section.src = os.path.join(dir_name, dir_list[image_no])
            image_section.update()
            get_caption(e)

    def change_image_left(e):
        global image_no

        if image_no > 0:
            image_no = image_no - 1
            image_section.src = os.path.join(dir_name, dir_list[image_no])
            image_section.update()
            get_caption(e)

    #View and edit captions
    def get_caption_file(dir_name, dir_list, image_no):

        caption_file = os.path.join(dir_name, dir_list[image_no])
        caption_file = caption_file.split('.')[0] + '.txt'
        return caption_file

    def get_caption(e):
        global dir_list, dir_name, image_no

        caption_file = get_caption_file(dir_name, dir_list, image_no)

        try:
            with open(file=caption_file, mode='r') as file:
                content = file.read()
                image_caption_textfield.value = content
                image_caption_textfield.update()
        except FileNotFoundError:
            image_caption_textfield.value = ""
            image_caption_textfield.update()

    def write_caption(e):
        global dir_list, dir_name, image_no

        caption_file = get_caption_file(dir_name, dir_list, image_no)
        print('Saved to '+ caption_file)

        with open(file=caption_file, mode='w') as file:
            file.write(image_caption_textfield.value)



    #IMAGE SECTION------------------
    image_section = ft.Image(
        #src="/home/redromnon/Pictures/Wallpapers/BlueNight.jpeg",
        border_radius=ft.border_radius.all(10)
    )

    #SELECTOR SECTION--------------
    dir_textfield = ft.TextField(label="Enter path to lora training dataset", icon=ft.icons.FOLDER, border_color=ft.colors.LIGHT_BLUE_50, on_submit=change_dir)
    
    image_caption_textfield = ft.TextField(label="caption", min_lines=2, border_color=ft.colors.AMBER_ACCENT, icon=ft.icons.EDIT, on_submit=write_caption)

    selector_section = ft.Column(
        [
            dir_textfield,
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_LEFT,
                        bgcolor=ft.colors.BLUE_800,
                        icon_size=30,
                        tooltip="Select left",
                        on_click=change_image_left
                    ),
                    ft.IconButton(
                        icon=ft.icons.ARROW_RIGHT,
                        bgcolor=ft.colors.BLUE_800,
                        icon_size=30,
                        tooltip="Select right",
                        on_click=change_image_right
                    )
                ],
                alignment="center",
                spacing=20
            ),
            image_caption_textfield
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.END,
    )


    #PAGE---------------
    page.theme_mode = "DARK"

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=image_section,
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=10
                ),
                ft.Divider(color=ft.colors.WHITE10, thickness=1),
                ft.Container(
                    content=selector_section,
                    alignment=ft.alignment.bottom_center,
                    padding=10
                ),
            ],
            expand=True,
            
        )
    )

    page.title = "LoRa Caption Creator"

    #page.vertical_alignment = ft.MainAxisAlignment.CENTER

ft.app(target=main, name="LoRa Caption Creator")
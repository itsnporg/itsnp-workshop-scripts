import asyncio
from time import time

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

file = pd.read_csv("example_names.csv", sep=",", encoding="UTF-8") #Load Names and Email from csv file using Pandas. 
                                                                   #Use example_names.csv file as reference



name = file["Name"].to_list()  # Convert name from csv to a list
email = file["Email"].to_list()  # Convert email from csv to a list

names_list = list(zip(name, email))  # Converting two lists into a tuple


def generate_image(name: str, email: str) -> None:
    """Function to generate Image using Pillow Module Python

    Args:
        name (str): Name (self explanatory)
        email (str): Email (self explanatory)
    """
    my_image = Image.open("example_cert.png")  # Loads Image using Pillow

    font = ImageFont.truetype("your_font_name.ttf", 250)  # Defining font for the image, SHould be on the same directory as this file for it to work
    name_title = str(name.title())

    """
    Maths to center the name on the image.
    """
    length = max([font.getlength(t) for t in name_title.split("\n")])
    height = 250 * len(name_title.split("\n"))
    xy = (2000 - length // 2, 1350 - height // 2) # Change 2000 and 1350 according to the image

    image_editable = ImageDraw.Draw(
        my_image
    )  # Initialize the rendering text on the image

    image_editable.text(
        xy=xy, text=name_title, fill=(255, 255, 255), font=font
    )  # Render the text on the image

    my_image.save(f"Certs/{email}.png")  # Save image to the Certs folder
    print(f"{name_title}'s Cert generated.")


async def main() -> None:
    """
    main module using asyncio to run the generate_image function
    """
    tasks = [
        asyncio.to_thread(generate_image, name=name, user_id=user_id)
        for (name, user_id) in names_list
    ]
    start_time = time()
    await asyncio.gather(*tasks)
    print(time() - start_time)


asyncio.run(main())

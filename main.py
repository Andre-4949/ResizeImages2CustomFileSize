import os
import threading
from urllib import request

from PIL import Image

ALLOWED_FILE_TYPES = [
    "png",
    "jpg",
    "jpeg"
]  # I didn't have time to test more ._.


def resize_img_to_custom_file_size(file, input_dir, output_dir, wanted_file_size=256000):
    path = input_dir + "/" + file
    print(path)
    img: Image = Image.open(path)
    file_size = os.path.getsize(path)  # the value which is shown in the explorer
    img_paths = []  # for deleting the imgs later

    # this is just for people who want to track each resizing step
    file_name = file.split(".")
    file_type = file_name.pop(-1)  # png, jpg or jpeg
    if not ALLOWED_FILE_TYPES.__contains__(file_type):
        print(f"This file format is not supported: {file_type}")
        if input("Do you want to continue, the results may not be what you expect. [Y|N]:").lower() != "y":
            exit(0)

    file_name = ".".join(file_name)

    i = 0
    while file_size > wanted_file_size:
        path_ = f"{output_dir}/{file_name}-{i}.{file_type}" if i != 0 else path
        img_paths.append(path_)

        if (wanted_file_size * 2) > file_size > wanted_file_size:

            # img size reduced by 1% of its size
            img = img.resize((int(img.size[0] * 0.99), int(img.size[1] * 0.99)))
        else:
            # img size reduced by 10% of its size
            img = img.resize((int(img.size[0] * 0.9), int(img.size[1] * 0.9)))

        img.save(path_)
        img = Image.open(path_)
        file_size = os.path.getsize(path_)
        i += 1

    img_paths = img_paths[1:-1] #remove first and last | first: original from input dir | last: the result
    for img_path in img_paths:
        os.remove(img_path)


def main():
    input_dir = "./pictures"
    output_dir = "./output"
    if not os.path.exists(input_dir):
        if input("Should we create an input directory for you? [Y|N]:").lower() == "y":
            os.mkdir(input_dir)
            print(f"Please now put your files in {input_dir} and restart the python script.")
            exit()
        else:
            input_dir = os.path.realpath(__file__)
            if input(
                    "The directory of this script will now be used as the working directory, shall we proceed? [Y|N]:").lower() != "y":
                exit(0)

    if not os.path.exists(output_dir):
        if input("Should we create an output directory for you? [Y|N]:").lower() == "y":
            os.mkdir(output_dir)
        else:
            output_dir = os.path.realpath(__file__)
            if input(
                    "The directory of this script will now be used as the "
                    "working directory, shall we proceed? [Y|N]").lower() != "y":
                exit(0)

    if input("Do you want to download a picture from a url? [Y|N]:\n").lower() == "y":
        i = 0
        print("""Please insert you link, a list of links (separated by space)
                             or n if you want to exit this loop (for the programmer of culture
                              there is of course the opportunity of pressing Ctrl+C :)):"""
              )
        while True:
            try:
                n = input("Please insert more arguments: ")
                if n == "n":
                    break
                else:
                    if n.split(" ").__sizeof__() == 0:
                        request.urlretrieve(n, input_dir + str(i) + "png")
                        i += 1
                    else:
                        for link in n.split(" "):
                            request.urlretrieve(link, input_dir + str(i) + "png")
                            i += 1
            except KeyboardInterrupt:
                break

    threadList = []

    # initialize threadlist
    file_size = None
    if input("Do you want to have different file sizes for different images [Y/N]:").lower() == "n":
        file_size = int(input("What file size do you want you image to be (You may use 'MB' or 'KB'): ")
                        .replace("M", "0" * 6).replace("K", "0" * 3).replace("B", "").replace(",",""))
    for file in os.listdir(input_dir):
        current_file_size = input(f"What file size do you want you image ({file}) to be (You may use 'MB' or 'KB'): ").replace("M","0" * 6).replace("K", "0" * 3).replace("B", "").replace(",","") if file_size == None else file_size
        t = threading.Thread(
            target=resize_img_to_custom_file_size,
            args=(file,
                  input_dir,
                  output_dir,
                  int(current_file_size)))
        threadList.append(t)

    # let's goo
    for t in threadList:
        t.start()

    # let's wait
    for t in threadList:
        t.join()
    print(f"""
    All images are resized.
    You may find the final results in:
    
    {os.path.realpath(output_dir)}""")


if __name__ == "__main__":
    main()

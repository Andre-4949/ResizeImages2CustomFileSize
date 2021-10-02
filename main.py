import os
import threading
from urllib import request
from PIL import Image


def resizeto256kb(file, input_dir):
    path = input_dir + "/" + file
    print(path)
    wantedfilesize = 256000
    img = Image.open(path)
    filesize = os.path.getsize(path)
    i = 0
    while filesize > wantedfilesize:
        if i != 0:
            path_ = str(i) + ".png"
        else:
            path_ = path
        if (wantedfilesize * 2) > filesize > wantedfilesize:
            img = img.resize((int(img.size[0] * 0.99), int(img.size[1] * 0.99)))
            img.save(path_)
            img = Image.open(path_)
            filesize = os.path.getsize(path_)
        else:
            img = img.resize((int(img.size[0] * 0.9), int(img.size[1] * 0.9)))
            img.save(path_)
            img = Image.open(path_)
            filesize = os.path.getsize(path_)
        i += 1
        print(f"{round((wantedfilesize / filesize) * 100, 2)}%")
        if filesize > wantedfilesize and path_ != path:
            try:
                os.remove(path_)
            except Exception as e:
                print(e)


def main():
    input_dir = "./pictures"

    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
        print(f"Please now put your files in {input_dir} and restart the python script.")
        exit()
    else:
        pass
    if input("Do you want to download a picture from a url? [Y|N]:\n").lower() == "y":
        i = 0
        while True:
            try:
                n = input("Your Link or type n if you want to stop:")
                if n == "n":
                    break
                else:
                    request.urlretrieve(n, input_dir + str(i) + "png")
                    i += 1
            except Exception as e:
                print(e)

    threadList = []
    print("Now the magic is happening!")
    for file in os.listdir(input_dir):
        t = threading.Thread(target=resizeto256kb, args=(file, input_dir))
        threadList.append(t)
        t.start()
    for t in threadList:
        t.join()
    print("Done!")


if __name__ == "__main__":
    main()

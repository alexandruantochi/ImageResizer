import tkinter
from tkinter import filedialog
import threading
import os
import glob
from PIL import Image
import multiprocessing

about_text_string = 'Choose the directory where your pictures\nare located and' \
                    ' add the percentage that\nyou want to resize them to.\n' \
                    '\nAuthor info:\nalexandru.antochi@gmail.com\nhttps://github.com/alexandruantochi\nwww.alexandruantochi.ro\n\n' \
                    'PayPal: https://www.paypal.me/AlexandruAntochi\n' \
                    'Send me an email if you use this app! :)\n' \
                    '\nThis app is open source and under the \nGNU General Public License'

askdir_entry_default = 'Enter dir location or browse..'

counter = 0


def update_counter(code):
    if code:
        counter_label.config(text=str(counter))
    else:
        counter_label.config(text='DONE!')


def worker1(file_list, percentage):
    """thread class"""
    global counter
    save_dir = askdir_entry.get() + '/ResizeImage/'
    for picture in file_list:
        image = Image.open(picture, mode='r')
        image_copy = image.copy()
        (width, height) = image.size
        filename = os.path.split(picture)[1]
        image_copy.thumbnail((width * (int(percentage) / 100), height * (int(percentage) / 100)))
        info_area.insert('end', '\n' + filename)
        info_area.see(tkinter.END)
        image_copy.save(save_dir + filename)
        counter += 1
        if counter % 3 == 0:
            update_counter(1)
    update_counter(0)


def resize():
    percentage = percentage_textbox.get()
    if not percentage:
        info_area.insert('end', 'Please write a percentage!')
        return
    askdir_entry.config(state='disabled')
    percentage_textbox.config(state='disabled')
    file_list = glob.glob(askdir_entry.get() + '/*.jp*g')
    info_area.insert('end', 'Found ' + str(len(file_list)) + ' pictures.\n')
    cpu = multiprocessing.cpu_count()
    info_area.insert('end', 'Number of threads: ' + str(cpu))
    info_area.insert('end', '\nResizing pictures..\n\n')
    if not os.path.exists(askdir_entry.get() + '/ResizeImage'):
        os.makedirs(askdir_entry.get() + '/ResizeImage')
    counter_label.config(text='-')
    for i in range(0, cpu):
        file_list_chunk = file_list[int(i*len(file_list)/cpu):int((i+1)*len(file_list)/cpu)]
        threading.Thread(target=worker1, args=(file_list_chunk, percentage)).start()


def ask_dir():
    askdir_entry.delete(0, 'end')
    dir_name = filedialog.askdirectory(mustexist=True, title='Choose pictures directory')
    askdir_entry.insert(0, dir_name)
    info_area.insert('end', dir_name + ' selected.\n')


def entry_clicked(event):
    if askdir_entry.get() == askdir_entry_default:
        askdir_entry.delete(0, 'end')


def aboutmenu():
    about_window = tkinter.Toplevel()
    about_window.title('About')
    about_text = tkinter.Text(about_window)
    about_text.insert('end', about_text_string)
    about_text.grid()
    about_text.config(state='disabled')
    about_window.geometry('390x250')
    about_window.resizable(width=False, height=False)


root = tkinter.Tk()

root.wm_title('Image Resizer')
root.resizable(width=False, height=False)
root.geometry('550x330')

browse_button = tkinter.Button(text='Browse..', command=ask_dir, height=1, width=15).grid(row=0, column=1, padx=10,
                                                                                          pady=15, sticky='w')

resize_button = tkinter.Button(text='Resize!', command=resize, height=1, width=15).grid(row=2, column=1, padx=10,
                                                                                        pady=15, sticky='w')

menubar = tkinter.Menu(root)
menubar.add_command(label='About', command=aboutmenu)
root.config(menu=menubar)

info_area = tkinter.Text(root, width=60, height=11)
info_area.grid(row=3, column=0, columnspan=2, sticky='ew', padx=(10, 0))
scrollbar = tkinter.Scrollbar(root)
scrollbar.grid(column=2, row=3, sticky='ns')
scrollbar.config(command=info_area.yview)
info_area.config(yscrollcommand=scrollbar.set)

askdir_entry = tkinter.Entry(root, width=60)
askdir_entry.insert(0, askdir_entry_default)
askdir_entry.grid(row=0, column=0, pady=20, padx=10, sticky='e')
askdir_entry.bind('<Button-1>', entry_clicked)

percentage_textbox = tkinter.Entry(root, width=3)
percentage_textbox.insert('end', '50')
percentage_textbox.grid(column=1, row=1, sticky='w', padx=10)
parcentage_label = tkinter.Label(root, text='Resize percentage [%]')
parcentage_label.grid(column=0, row=1, sticky='e', padx=10)

counter_label = tkinter.Label(root)
counter_label.grid(column=0, row=2, sticky='w', padx=10)

root.mainloop()

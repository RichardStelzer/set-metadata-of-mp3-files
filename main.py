from tkinter import *  # GUI
from tkinter import messagebox

from mutagen.mp3 import EasyMP3 as MP3  # for writing metadata to file
from mutagen.easyid3 import EasyID3
import mutagen.id3

import pyperclip
import glob
import os

# global audio_input, audio_tagged_output, counter, max_file_count, all_filepaths
counter = 1

audio_path = os.path.join(os.getcwd(), "audio\\")
audio_input = audio_path + "audio_input\\"
audio_tagged_output = audio_path + "audio_tagged_output\\"
max_file_count = len(glob.glob(audio_input + "\\*.mp3"))
all_filepaths = glob.glob(audio_input + "\\*.mp3")

# create directories
if not os.path.exists(audio_input):
    os.makedirs(audio_input)
    os.makedirs(audio_tagged_output)
    print('PUT AUDIO FILES IN THE audio/audio_input FOLDER TO START TAGGING')


def about_dialog():
    m_text = "\
************************\n\
Author: Richard Stelzer\n\
Version: 1.337\n\
************************"
    messagebox.showinfo(message=m_text, title="Infos")


fields = 'Directory', 'Filepath', 'Filename', 'Artist', 'Title'


def fetch(entries):
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text))


def load(entries):
    global audio_path


def make_form(window, fields):
    entries = []
    for field in fields:
        row = Frame(window)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append([field, ent])
    return entries


def fill_form(entries):
    # global counter, audio_input, max_file_count, all_filepaths
    print('FILE_ID: ', counter)
    print('File_Count', max_file_count)
    print(audio_input)

    if counter > max_file_count:
        print('No audio files in the directory!!! Exiting Program')
        quit()

    entries[0][1].delete(0, 'end')
    entries[1][1].delete(0, 'end')
    entries[2][1].delete(0, 'end')
    entries[3][1].delete(0, 'end')
    entries[4][1].delete(0, 'end')

    # replace Backslashes created by glob.glob to forward slashes
    current_filepath = all_filepaths[counter - 1]
    filename = current_filepath.split("\\")[-1][:-4]  # get filename & remove 4 last characters ".mp3"

    # insert data into the form
    entries[0][1].insert(0, audio_input)
    entries[1][1].insert(0, current_filepath)
    entries[2][1].insert(0, filename)

    filename_replaced = filename.replace('_', ' ').strip()

    try:  # split filename in artist & title by splitting at "-"
        # simplify by removing keywords
        keywords = ['Music Video', 'MUSIC VIDEO', 'OFFICIAL', 'official', 'Official', 'Video', 'VIDEO',
                    'Official Audio', 'OFFICIAL LIVE VIDEO', 'official Video', 'Official video', 'OFFICIAL TRACK',
                    'Official Track', 'official track', 'with Lyrics', 'with lyrics', 'With Lyrics', 'WITH LYRICS',
                    'Lyrics', 'Lyric', 'HQ', 'hq', 'HD', 'Official Video', 'OFFICIAL VIDEO', 'Lyrics', 'LYRICS',
                    'lyric\'s', 'lyrics', 'Official Music Video', 'OFFICIAL MUSIC VIDEO', 'Official Lyric Video',
                    'OFFICIAL LYRIC VIDEO', 'Lyric Video', 'LYRIC VIDEO', '()', '( )', '[]', '[ ]']

        title_parts = filename.split('-', 1)  # split maximal 1 time at '-'
        artist = title_parts[0].replace('_', ' ').strip()
        title = title_parts[1].replace('_', ' ').strip()
        for r in keywords:
            artist = artist.replace(r, '')
            title = title.replace(r, '')
        artist.strip()
        title.strip()

    except:
        print('Filename includes no delimiter - \n using filename as suggestion')
        artist = filename_replaced
        title = filename_replaced
    # insert data into the form
    entries[3][1].insert(0, artist)
    entries[4][1].insert(0, title)


def save_tags(entries):
    global counter, audio_input, audio_tagged_output
    print(counter)
    filepath = entries[1][1].get()
    new_filename = entries[3][1].get() + ' - ' + entries[4][1].get() + '.mp3'
    new_filepath = audio_tagged_output + new_filename
    print('audiopath: ', audio_input)
    print('filepath: ', filepath)
    print('new_filename: ', new_filename)
    print('new_filepath: ', new_filepath)
    mp3file = MP3(filepath, ID3=EasyID3)
    print('MP3FILE:  ', mp3file)
    try:
        mp3file.add_tags(ID3=EasyID3)
    except mutagen.id3.error:
        print('has tags ... removing them')
        mp3file.delete()
        mp3file.save()
        # mp3file.add_tags(ID3=EasyID3)

    artist = entries[3][1].get()
    title = entries[4][1].get()

    mp3file['artist'] = artist
    mp3file['title'] = title
    mp3file.save()

    print('filepath', filepath)
    print('new filepath', new_filepath)
    try:
        os.remove(new_filepath)
        print('Removed already existing file named: ' + new_filename)
    except:
        print('No file in ' + new_filepath + ' named ' + new_filename + ' found')
    os.rename(filepath, new_filepath)  # os.rename("c:/a", "c:/b/a") # move a to b
    counter += 1
    print('FILE_ID_END: ', counter)
    pyperclip.copy(artist)
    fill_form(entries)  # move to next audio file


if __name__ == "__main__":
    window = Tk()  # create window
    window.title('Set Metadata for Audio Files')

    menubar = Menu(window)
    file_menu = Menu(menubar, tearoff=0)
    help_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label='Restart', command=window.quit)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=window.quit)
    help_menu.add_command(label='About', command=about_dialog)
    menubar.add_cascade(label='File', menu=file_menu)
    menubar.add_cascade(label='About', menu=help_menu)

    ents = make_form(window, fields)

    # window.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = Button(window, text='Load .mp3', command=(lambda: fill_form(ents)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(window, text='Save .mp3', command=(lambda: save_tags(ents)))
    b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(window, text='Next .mp3', command=(lambda: fill_form(ents)))
    b3.pack(side=LEFT, padx=5, pady=5)
    b4 = Button(window, text='Print to Terminal', command=(lambda e=ents: fetch(e)))
    b4.pack(side=LEFT, padx=5, pady=5)
    b5 = Button(window, text='Quit', command=window.quit)
    b5.pack(side=LEFT, padx=5, pady=5)

    window.config(menu=menubar)
    window.mainloop()

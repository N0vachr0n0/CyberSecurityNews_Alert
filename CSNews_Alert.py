#!/usr/bin/python3

'''
CSNEWS stands for CyberSecurity News !!
Stay in alert with CSNews !
Check News from several websites in one instance.

By N0vachr0n0
Github: https://github.com/N0vachr0n0
'''

from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from datetime import datetime, date, timedelta
from tkinter.messagebox import *
from threading import Thread
import webbrowser
import requests
import time

sites = ["https://cyberguerre.numerama.com/feed/", "https://feeds.feedburner.com/TheHackersNews?format=xml",
         "https://rss.packetstormsecurity.com/news/", "https://www.zdnet.fr/blogs/cybervigilance/rss/",
         "https://www.zataz.com/rss/zataz-news.rss", "https://portswigger.net/daily-swig/rss",
         "https://threatpost.com/feed"]

# title_list[0] and link_list[0] correspond to the title and the website of article
title_list_today = []
link_list_today = []

title_list_yest = []
link_list_yest = []

title_list_old = []
link_list_old = []


root = Tk()
root.title("CyberSecurity News")
root.geometry('650x450')
root.resizable(0, 0)  # Block resizing of window
root.config(cursor="pirate")


win_loading = Tk()
win_loading.geometry('250x100')
win_loading.title("Loading...")

msg = Label(win_loading, text="WAIT PLEASE")

# Progress bar widget
progress = Progressbar(win_loading, orient=HORIZONTAL,
                       length=100, mode='determinate')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='HOT')
tabControl.add(tab2, text='RECENT')
tabControl.add(tab3, text='OLD')
tabControl.add(tab4, text='CREDIT')
tabControl.pack(expand=1, fill="both")

scrollbar = Scrollbar(tab1)
scrollbar_re = Scrollbar(tab2)
scrollbar_old = Scrollbar(tab3)

scrollbar.pack(side=RIGHT, fill=Y)
scrollbar_re.pack(side=RIGHT, fill=Y)
scrollbar_old.pack(side=RIGHT, fill=Y)

article_hot = Listbox(tab1, selectbackground="pink", width=80, yscrollcommand=scrollbar.set)
article_recent = Listbox(tab2, selectbackground="pink", width=80, yscrollcommand=scrollbar_re.set)
article_old = Listbox(tab3, selectbackground="pink", width=80, yscrollcommand=scrollbar_old.set)

credit = "CyberSecurity News\n\nMade by N0vachr0n0\nThanks for downloading,\
 please share ;)\n\nGithub: https://github.com/N0vachr0n0"

Label(tab4, text=credit, justify="center").grid(padx=180, pady=110)


# Function responsible for the updation
# of the progress bar value
def bar():
    progress['value'] = 20
    win_loading.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 40
    win_loading.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 50
    win_loading.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 60
    win_loading.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 80
    win_loading.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 100
    win_loading.update_idletasks()
    time.sleep(0.5)


# Look for title and link of articles in a XML doc
def cooking(url):
    try:
        response = requests.get(url)
    except:
        showerror(title="CONNECTION ERROR", message="Please check your internet connection and try again.")
        showinfo(title="CREDIT", message="Made by N0vachr0n0\nGoodbye Friend ;) ")
        root.destroy()

    soup = BeautifulSoup(response.content, "xml")

    for item in soup.find_all("item"):
        pubdate = item.find("pubDate")
        pubdate = int((str(pubdate.text))[5:7])
        # print(pubdate)
        if pubdate == (datetime.now()).day:
            title = item.find("title")
            link = item.find("link")

            title_list_today.append(">_ " + title.text)
            link_list_today.append(link.text)

        elif pubdate == (date.today()-timedelta(1)).day:
            title = item.find("title")
            link = item.find("link")

            title_list_yest.append(">_ " + title.text)
            link_list_yest.append(link.text)
        else:
            title = item.find("title")
            link = item.find("link")

            title_list_old.append(">_ " + title.text)
            link_list_old.append(link.text)


# Retrieves index of article title from listbox and go to website
def go_recent(event):
    cs = article_recent.curselection()
    for pos in cs:
        webbrowser.open(link_list_yest[pos])


def go_hot(event):
    cs = article_hot.curselection()
    for pos in cs:
        webbrowser.open(link_list_today[pos])


def go_old(event):
    cs = article_old.curselection()
    for pos in cs:
        webbrowser.open(link_list_old[pos])


# Actualization (look for new articles and insert into the lists)
def refresh():
    showinfo(title="REFRESHING...", message="We are looking for News ;) ")
    root.config(cursor="watch")

    title_list_old.clear()
    link_list_old.clear()
    title_list_today.clear()
    link_list_today.clear()
    title_list_yest.clear()
    link_list_yest.clear()

    article_old.delete(0, END)
    article_hot.delete(0, END)
    article_recent.delete(0, END)

    for i in range(len(sites)):
        cooking(sites[i])

    # Insertion in listbox
    for x in range(len(title_list_today)):
        article_hot.insert(END, title_list_today[x])

    for x in range(len(title_list_yest)):
        article_recent.insert(END, title_list_yest[x])

    for x in range(len(title_list_old)):
        article_old.insert(END, title_list_old[x])

    article_old.pack(expand=1, side=LEFT, fill=BOTH)
    article_hot.pack(expand=1, side=LEFT, fill=BOTH)
    article_recent.pack(expand=1, side=LEFT, fill=BOTH)

    root.config(cursor="pirate")
    showinfo(title=INFO, message="DOUBLE-CLICK OR PRESS ENTER ON A TITLE TO OPEN WEBSITE XD")


if __name__ == '__main__':
    root.withdraw()  # Hide root window ;)

    msg.pack(padx=10, pady=10)
    progress.pack(pady=10)
    bar()
    win_loading.destroy()

    control_thread = Thread(target=refresh, daemon=True)  # Start Refresh function in parallel
    control_thread.start()

    root.deiconify()  # Show root window
    Button(root, text='REFRESH', command=refresh).pack(side=BOTTOM, padx=5, pady=5)

    # Waiting for Double-click or Key ENTER to go on the website
    article_hot.bind("<Double-1>", go_hot)
    article_hot.bind("<Return>", go_hot)

    article_recent.bind("<Double-1>", go_recent)
    article_recent.bind("<Return>", go_recent)

    article_old.bind("<Double-1>", go_old)
    article_old.bind("<Return>", go_old)

    scrollbar.config(command=article_hot.yview)
    scrollbar_re.config(command=article_recent.yview)
    scrollbar_old.config(command=article_old.yview)

    mainloop()

import random
import threading
import time
from tkinter import *
from tkinter import ttk
# from pynput.mouse import Button, Controller
from pynput import keyboard




class KeyLogger:

    def __init__(self):
        self.__key_log = []
        self.__press_thread = 0
        self.__release_thread = 0
        self.__stopped = False

    def record_presses(self):
        print('record_presses()')

        def on_key_press(key):
            # self.__key_log.append(['press', key, time.time()])
            # if self.__stopped == True:
            #     return False
            # else:
            #     return
            if self.__stopped == True:
                return False
            self.__key_log.append(['press', key, time.time()])
            return


        # while True:
        #     with keyboard.Listener(on_press=on_key_press) as press_listener:  # setting code for listening key-press
        #         press_listener.join()
        #     print('PRESS ITERATION DONE')
        # while True:
        with keyboard.Listener(on_press=on_key_press) as press_listener:  # setting code for listening key-press
            press_listener.join()
        # print('PRESS ITERATION DONE')



    def record_releases(self):
        print('record_releases()')

        def on_key_release(key):
            # self.__key_log.append(['release', key, time.time()])
            # if self.__stopped == True:
            #     return False
            # else:
            #     return
            if self.__stopped == True:
                return False
            self.__key_log.append(['release', key, time.time()])
            return

        # while True:
        #     with keyboard.Listener(on_release=on_key_release) as release_listener:  # setting code for listening key-release
        #         release_listener.join()
        #     print('RELEASE ITERATION DONE')
        # while True:
        with keyboard.Listener(on_release=on_key_release) as release_listener:  # setting code for listening key-release
            release_listener.join()
        # print('RELEASE ITERATION DONE')


    def record_key_log(self):
        print('record_key_log()')
        self.__stopped = False
        self.__key_log = []
        self.__key_log.append(['start', time.time()])
        self.__press_thread = threading.Thread(target=self.record_presses, args=())
        self.__release_thread = threading.Thread(target=self.record_releases, args=())
        self.__press_thread.start()
        self.__release_thread.start()

        # def on_key_press(key):  # what to do on key-press
        #     print('just got here')
        #     self.__key_log.append(('press', time.time()))
        #     print('about to leave')
        #     return
        #
        # def on_key_release(key):  # what to do on key-release
        #     # time_taken = round(time.time() - t, 2)  # rounding the long decimal float
        #     # print("The key", key, " is pressed for", time_taken, 'seconds')
        #     # return False  # stop detecting more key-releases
        #     self.__key_log.append(('release', time.time()))
        #     return
        #
        # while True:
        #     print('before anything')
        #     with keyboard.Listener(on_press=on_key_press) as press_listener:  # setting code for listening key-press
        #         press_listener.join()
        #     print('middle')
        #     with keyboard.Listener(on_release=on_key_release) as release_listener:  # setting code for listening key-release
        #         release_listener.join()
        #     print('after')

    def stop_key_log(self):
        print('stop_key_log()')
        # self.__press_thread.join()
        # self.__release_thread.join()
        self.__stopped = True

    def play_key_log(self):
        print('play_key_log()')
        print(self.__key_log)
        my_keyboard = keyboard.Controller()
        # for index in range(1, len(self.__key_log)):


    def format_key_log(self):
        print('format_key_log()')
        for index in range(1, len(self.__key_log)):
            # print(index)
            self.__key_log[index][2] = self.__key_log[index][2]-self.__key_log[0][1]
        # print(self.__key_log)
        for index in range(1, len(self.__key_log)):
            self.__key_log[index][2] = self.__key_log[index][2]-self.__key_log[1][2]


def main():
    key_logger = KeyLogger()
    root = Tk()
    root.title('KeyLogger')
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text='Record', command=key_logger.record_key_log).grid(row=0, column=0)
    ttk.Button(frm, text='Stop', command=key_logger.stop_key_log).grid(row=0, column=1)
    ttk.Button(frm, text='Play', command=key_logger.play_key_log).grid(row=0, column=2)

    ttk.Button(frm, text='Format', command=key_logger.format_key_log).grid(row=0, column=3)

    root.mainloop()


if __name__ == '__main__':
    main()

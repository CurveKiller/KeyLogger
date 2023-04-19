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
        self.__play_thread = 0

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

        with keyboard.Listener(on_press=on_key_press) as press_listener:  # setting code for listening key-press
            press_listener.join()



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

        with keyboard.Listener(on_release=on_key_release) as release_listener:  # setting code for listening key-release
            release_listener.join()


    def record_key_log(self):
        print('record_key_log()')
        self.__stopped = False
        self.__key_log = []
        self.__key_log.append(['start', time.time()])
        self.__press_thread = threading.Thread(target=self.record_presses, args=())
        self.__release_thread = threading.Thread(target=self.record_releases, args=())
        self.__press_thread.start()
        self.__release_thread.start()

    def stop_key_log(self):
        print('stop_key_log()')
        # self.__press_thread.join()
        # self.__release_thread.join()
        self.__stopped = True


    def play_key_log_thread(self):
        my_keyboard = keyboard.Controller()
        # for index in range(1, len(self.__key_log)):
        KEY_PRESS = 'press'
        KEY_RELEASE = 'release'
        for action in self.__key_log:
            if len(action) == 2:
                # this is a key press or release
                if action[0] == KEY_PRESS:
                    # this is a key press
                    my_keyboard.press(action[1])
                elif action[0] == KEY_RELEASE:
                    # this is a key release
                    my_keyboard.release(action[1])
            else:
                # this is a wait
                time.sleep(action[0])

    def play_key_log(self):
        print('play_key_log()')
        print(self.__key_log)
        self.__play_thread = threading.Thread(target=self.play_key_log_thread, args=())
        self.__play_thread.start()

    def format_key_log(self):
        print('format_key_log()')
        # for index in range(1, len(self.__key_log)):
        #     # print(index)
        #     self.__key_log[index][2] = self.__key_log[index][2]-self.__key_log[0][1]
        # print(self.__key_log)
        # for index in range(1, len(self.__key_log)):
        #     self.__key_log[index][2] = self.__key_log[index][2]-self.__key_log[1][2]

        new_key_log = []
        for index in range(1, len(self.__key_log)):
            if index == 1:
                new_key_log.append([self.__key_log[index][0], self.__key_log[index][1]])
            else:
                new_key_log.append([self.__key_log[index][2] - self.__key_log[index-1][2]])
                new_key_log.append([self.__key_log[index][0], self.__key_log[index][1]])
        # print(new_key_log)
        self.__key_log = new_key_log
        # new_key_log = []
        # secs_since = 0
        # for index in range(1, len(self.__key_log)):
        #     if index==1:
        #         new_key_log.append([self.__key_log[index][0], self.__key_log[index][1]])
        #         secs_since = self.__key_log[index][2]
        #     else:
        #         # append seconds delay since
        #         # new_key_log.append([self.__key_log[index][2]])
        #         # new_key_log.append([self.__key_log[index][2] - secs_since])
        #         new_key_log.append([secs_since])
        #
        #         # update seconds_since last move
        #         secs_since = self.__key_log[index][2] - secs_since
        #
        #         # append next move
        #         new_key_log.append([self.__key_log[index][0], self.__key_log[index][1]])
        # print(new_key_log)

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

    ttk.Label(frm, text='abc').grid(row=1, column=0)
    ttk.Entry(frm).grid(row=1, column=1)
    root.mainloop()


if __name__ == '__main__':
    main()

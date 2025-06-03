"""
Name: Humberto Torralba
UTEID: ht7665

On my honor, Humberto Torralba, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

1. What is the purpose of your program?
The purpose of this program is to give the user a GUI allowing them to quickly
and easily record macros/hotkeys. Many similar programs today require you to
buy a specific mouse or keyboard then either with software or hardware, let
the user record macros, and other only software based solutions are a little
clunky and not as intuitive <AutoHotKey>. This program tends to fill in this
use case gap with a simple, light, free, easy to use gui that anybody can use
despite their technical knowledge.

2. List the major features of your program:
1) Allows the user to record key presses and key releases on their keyboard.
2) Can play back recorded key press/releases an unlimited number of times.
3) Maintains the time spent between keyboard interactions that way when played
back it perfectly mimics the user's input.

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)
Requires the installation of 'pynput' <pip install pynput>
- Speficically requires the keyboard module from pynput.
Also uses the following standard modules:
- random
- threading
- time
- tkinter

4. List the things your learned while doing this program. Python features,
   techniques, third party modules, etc.
I learned how multithreading is handled in python and how to utilize the
threading module in order to multithread my project. I realized that if the
main thread is listening for keypresses, than the GUI is left unresponsive.
I learned and gained more experience with tkinter in general. I specifically
learned about some of the limitations of tkinter, such as how binding
key presses in tkinter by the root does not allow the python file as a whole
detect key presses outside of the tkinter window. Instead I needed to use the
pynput module for this. I learned more about the time module in python and got
practice using it.

5. What was the most difficult thing you had to overcome or learn
   to get this program to work?
The most difficult part of this program was multi threading the listening for
keyboard presses and releases. This came to a surprise to me since I thought
there would be a simpler method for doing so, <import answer>, but instead I
had to code it myself. One specific hurdle I overcame was synchronizing and
communicating between threads (root-thread, press-thread, release-thread) was
more difficult since I thought it would be because debugging can be rather
ambiguous at times. What I had to do was deep read the pynput documentation
and threading documentation in order to see how the threads were constructed
and maintained within the PythonVirtualEnvironment and how and when pynput was
actually listening for keyboard interactions.

6. What features would you add next?
I would add hotkeys to for every button for two reasons:
- Make it completely accessible while minimized.
- Eliminate the need for the start-delay.
I want to touch base on the original proposal, when I was writing the proposal
I thought it would be extremely simple to detect keypresses (hotkeys like
Shift+Esc) and to bind them to buttons. This turned out to not be true since
when binding keys to buttons as shown in class through Tkinter, those keys are
only detected while the tkinter window is active, the primary application
viewed on your system. Now with pynput I was able to work around this
limitation for detecting key-presses and key-releases *when recording the
macros, not for activating the buttons*. I could work around this but the
added complexity would be quite huge since I would have to constantly have to
manage the communication of 4+ threads (tkinter-thread, press-thread,
release-thread, button-thread). Given more time, I will likely do this over
the Summer.
Another feature I would add is letting the user save and replay previously
recorded macros onto/from their device. This was also outlined in my proposal
but wrapping my head around the multithreading that this version already
requires took alot more time than I thought.
Lastly another feature I would add would be post-macro-editor where the user
could view and edit a recorded macro before playing it. I think this could be
implemented with a Tkinter 'listbox'. It would show all of the key presses,
key releases and delays between those actions. The user could then edit or
remove any of those items before playing the macro.

This was a fun project that really allowed me to stretch my knowledge in
various topics. I think I bit off more than I could chew in my proposal:P

"""


import random
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk
from pynput import keyboard


def main():
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
                if self.__stopped:
                    return False
                self.__key_log.append(['press', key, time.time()])
                return

            # setting code for listening key-press
            with keyboard.Listener(on_press=on_key_press) as press_listener:
                press_listener.join()

        def record_releases(self):
            print('record_releases()')

            def on_key_release(key):
                if self.__stopped:
                    return False
                self.__key_log.append(['release', key, time.time()])
                return

            # setting code for listening key-release
            with keyboard.Listener(on_release=on_key_release) as \
                    release_listener:
                release_listener.join()

        def record_key_log(self, event=None):
            print('record_key_log()')

            # update stopped so the press and release threads don't
            # immediately close
            self.__stopped = False

            # clear the key_log
            self.__key_log = []

            # add the start time for formatting later
            self.__key_log.append(['start', time.time()])
            self.__press_thread = \
                threading.Thread(target=self.record_presses, args=())
            self.__release_thread = \
                threading.Thread(target=self.record_releases, args=())
            self.__press_thread.start()
            self.__release_thread.start()

            # enable the stop button and disable the record and play buttons
            record_button.config(state='disabled')
            stop_button.config(state='normal')
            play_button.config(state='disabled')

        def stop_key_log(self):
            print('stop_key_log()')

            # update stopped so the press and release threads will stop
            # taking input and close
            self.__stopped = True

            # format the key_log to a more usable format
            self.format_key_log()

            # enable the record and play buttons and disable the stop button
            record_button.config(state='normal')
            stop_button.config(state='disabled')
            play_button.config(state='normal')

        def play_key_log_thread(self):
            my_keyboard = keyboard.Controller()
            KEY_PRESS = 'press'
            KEY_RELEASE = 'release'
            # print(f'fdsa{repeat_str.get()}')
            if repeat_bool.get():
                for repeat_index in range(0, int(repeat_str.get())):
                    for action_index in range(len(self.__key_log)):
                        action = self.__key_log[action_index]
                        if len(action) == 2:
                            # this is a key press or release
                            if action[0] == KEY_PRESS:
                                # this is a key press
                                print(f'press = {action[1]}')
                                my_keyboard.press(action[1])
                            elif action[0] == KEY_RELEASE:
                                # this is a key release
                                print(f'release = {action[1]}')
                                my_keyboard.release(action[1])
                        else:
                            # this is a wait
                            if(action_index!=0 and fast_playback_bool.get()):
                                print(f'wait = {fast_playback_times[fast_playback_combo_box.current()]}')
                                time.sleep(float(fast_playback_times[fast_playback_combo_box.current()]))
                            else:
                                print(f'wait = {action[0]}')
                                time.sleep(action[0])
            else:
                for action_index in range(len(self.__key_log)):
                    action = self.__key_log[action_index]
                    if len(action) == 2:
                        # this is a key press or release
                        if action[0] == KEY_PRESS:
                            # this is a key press
                            print(f'press = {action[1]}')
                            my_keyboard.press(action[1])
                        elif action[0] == KEY_RELEASE:
                            # this is a key release
                            print(f'release = {action[1]}')
                            my_keyboard.release(action[1])
                    else:
                        # this is a wait
                        if(action_index!=0 and fast_playback_bool.get()):
                            print(f'wait = {fast_playback_times[fast_playback_combo_box.current()]}')
                            time.sleep(float(fast_playback_times[fast_playback_combo_box.current()]))
                        else:
                            print(f'wait = {action[0]}')
                            time.sleep(action[0])

        def play_key_log(self, event=None):
            print('play_key_log()')
            print(self.__key_log)

            # play out the macro in a different thread so that the window
            # stays responsive
            self.__play_thread =\
                threading.Thread(target=self.play_key_log_thread, args=())
            self.__play_thread.start()

        def format_key_log(self):
            print('format_key_log()')

            new_key_log = []

            # add the start-delay time
            new_key_log.append([float(wait_times[wait_combo_box.current()])])

            # compute the difference between the actions and reformat the list
            # into new_key_log
            for index in range(1, len(self.__key_log)):
                if index == 1:
                    new_key_log.append([self.__key_log[index][0],
                                        self.__key_log[index][1]])
                else:
                    new_key_log.append([self.__key_log[index][2] -
                                        self.__key_log[index - 1][2]])
                    new_key_log.append([self.__key_log[index][0],
                                        self.__key_log[index][1]])

            # have the old key_log point to the new_key_log
            self.__key_log = new_key_log

    key_logger = KeyLogger()
    root = Tk()
    root.title('KeyLogger')

    instr_frm = ttk.LabelFrame(root, text='Instructions', padding=5)
    instr_frm.grid(row=0, column=0, sticky='N')
    ttk.Label(instr_frm, text='Press Record to begin recording a macro.')\
        .grid(row=0, column=0, sticky='W')
    ttk.Label(instr_frm, text='Press Stop to the recording.')\
        .grid(row=1, column=0, sticky='W')
    ttk.Label(instr_frm, text='Press Play to playback the macro.')\
        .grid(row=2, column=0, sticky='W')
    ttk.Label(instr_frm, text='Set the start delay (seconds) to\n'
                              'adjust how late the macro starts after playing.')\
        .grid(row=3, column=0, sticky='W')
    ttk.Label(instr_frm, text='Tip: The program only tracks keyboard\n'
                              'actions so use mouse input to move\n'
                              'between windows.') \
        .grid(row=4, column=0, sticky='W')


    button_frm = ttk.LabelFrame(root, text='Actions', padding=5)
    button_frm.grid(row=1, column=0, sticky='N')

    record_button = ttk.Button(button_frm, text='Record',
                               command=key_logger.record_key_log)
    record_button.grid(row=0, column=0)
    stop_button = ttk.Button(button_frm, text='Stop',
                             command=key_logger.stop_key_log, state='disabled')
    stop_button.grid(row=0, column=1)
    play_button = ttk.Button(button_frm, text='Play',
                             command=key_logger.play_key_log, state='disabled')
    play_button.grid(row=0, column=2)

    play_settings_frm = ttk.LabelFrame(root, text='Play Settings', padding=5)
    play_settings_frm.grid(row=0, column=1, sticky='N')


    wait_label = ttk.Label(play_settings_frm, text='      Start Delay')
    wait_label.grid(row=0, column=0, sticky='W')

    wait_str = tkinter.StringVar()
    wait_combo_box = ttk.Combobox(play_settings_frm, width=10, textvariable=wait_str, state='readonly')
    wait_combo_box.grid(row=0, column=1)
    wait_times = ('0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0')
    wait_combo_box['values'] = wait_times
    wait_combo_box.current(4)

    fast_playback_bool = tkinter.BooleanVar()
    fast_playback_checkbox = ttk.Checkbutton(play_settings_frm, text='Fast Playback', variable=fast_playback_bool)
    fast_playback_checkbox.grid(row=1, column=0, sticky='W')


    repeat_bool = tkinter.BooleanVar(value=False)

    repeat_checkbox = ttk.Checkbutton(play_settings_frm, text='Repeat', variable=repeat_bool)
    repeat_checkbox.grid(row=2, column=0, sticky='W')

    def _validate(P):
        print(f'validate = {P}')
        return P.isdigit()

    digit_validation = root.register(_validate)
    repeat_str = tkinter.IntVar()
    repeat_spin_box = ttk.Spinbox(play_settings_frm, width=10, textvariable=repeat_str, from_=0, to=300, state='disabled')
    repeat_spin_box.config(validate='key', validatecommand=(digit_validation, '%P'))
    repeat_spin_box.grid(row=2, column=1)

    def update_repeat_state(*args):
        if repeat_bool.get():
            repeat_spin_box.config(state='normal')
            repeat_checkbox.config(text='Repeat        #:')
        else:
            repeat_spin_box.config(state='disabled')
            repeat_checkbox.config(text='Repeat')

    repeat_bool.trace('w', update_repeat_state)

    fast_playback_str = tkinter.StringVar()
    fast_playback_combo_box = ttk.Combobox(play_settings_frm, width=10, textvariable=fast_playback_str,
                                           state='disabled')
    fast_playback_combo_box.grid(row=1, column=1)
    fast_playback_times = ('0.0', '0.03', '0.06', '0.09', '0.12', '0.15', '0.18', '0.21', '0.24', '0.27', '0.3', '0.33',
                           '0.36', '0.39', '0.42', '0.45', '0.48')
    fast_playback_combo_box['values'] = fast_playback_times
    fast_playback_combo_box.current(3)

    def update_fast_playback_state(*args):
        if fast_playback_bool.get():
            fast_playback_combo_box.config(state='readonly')
        else:
            fast_playback_combo_box.config(state='disabled')

    fast_playback_bool.trace('w', update_fast_playback_state)

    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()

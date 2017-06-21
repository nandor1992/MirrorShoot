from tkinter import *
import queue
class Console(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)
        self.text = Text(self, wrap='word', **kwargs)
        self.text.pack()
        self.text.config(state='disabled')
        self.sequence = ['-', '\\', '|', '/']
        self.load = False
        self.queue = queue.Queue()
        self.update_me()
    def write(self, line, link=None):
        self.queue.put((line,link))
    def clear(self):
        self.queue.put((None, None))
    def update_me(self):
        try:
            while 1:
                line, link = self.queue.get_nowait()

                self.text.config(state='normal')
                if line is None:
                    self.text.delete(1.0, END)
                elif link and link == 'loader':
                    self.load = True
                    self.text.delete(self.text.index("end-2c"))
                    self.text.insert(self.text.index("end-1c"), str(line))
                else:
                    if self.load:
                        self.text.delete(self.text.index("end-2c"))
                        self.text.insert(self.text.index("end-1c"), str(line))
                    else:
                        self.text.insert(END, str(line))
                    self.load = False
                self.text.see(END)
                self.update_idletasks()
                self.text.config(state='disabled')
        except queue.Empty:
            pass
        self.after(100, self.update_me)
        if self.load:
            self.queue.put((self.sequence[0], 'loader'))
            self.sequence.append(self.sequence.pop(0))

if __name__ == '__main__':
    # testing application
    import time
    root = Tk()
    console = Console(root)
    console.pack()

    def load_it():
        console.write('Loading World...', 'loader')
        time.sleep(3)
        console.write('Done')

    import threading
    t = threading.Thread(target=load_it)
    t.daemon = True
    t.start()

    root.mainloop()
    exit()
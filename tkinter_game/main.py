## 수정 안해도됨
from app import *
def on_closing():
    global interrupt
    if messagebox.askokcancel("Quit", "Quit?"):
        root.quit()
        interrupt = 0

if __name__ == "__main__":
    global interrupt
    interrupt = 1
    width = 4
    root = Tk()

    while True:
        app = App(root, width)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        if app.continue_game == 0 or interrupt == 0:
            break
            root.destroy()
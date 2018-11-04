## 수정 안해도됨
from maintable import *
from conveyor import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
import os

class App(Frame):    
    picture_image = [] # 메인 테이블용 도형 이미지
    alphabet_image = [] # 메인 테이블용 알파벳 이미지
    resized_picture = [] # 컨베이어용 도형 이미지
    continue_game = 1
    
    def __init__(self, master, n):
        super(App, self).__init__()
        self.master = master # root를 parent로
        self.n = n
        self.create_images() # 이미지 읽어와서 저장

        # Maintable frame widget 생성
        self.table = Maintable(self, self.picture_image, self.alphabet_image, self.n)
        self.table.grid(row=0, column=0, pady=(10,20))

        # Conveyor frame widget 생성
        self.conveyor = Conveyor(self, self.resized_picture, self.n)
        self.conveyor.grid(row=1, column=0)


    # 이미지 파일을 읽어와서 이미지 객체를 생성하고 리스트에 저장하는 부분

    # 생성된 이미지 객체 리스트에는 추가적인 변경이 없고, index를 통해 randomize
    def create_images(self):
        self.picture_image = list(Image.open("picture\\%d.JPG" % (i+1)) for i in range(self.n*self.n))
        self.alphabet_image = list(PhotoImage(file="alphabet\\%d.GIF" % (i+1)) for i in range(self.n*self.n))
        self.resized_picture = list(self.picture_image[i].resize((50,50), Image.ANTIALIAS) for i in range(self.n*self.n))
        self.resized_picture = list(ImageTk.PhotoImage(self.resized_picture[i]) for i in range(self.n*self.n))
        self.picture_image = list(ImageTk.PhotoImage(self.picture_image[i]) for i in range(self.n*self.n))

    # 게임 종료시 처리 부분
    def quit_game(self, win):
        if win == True:
            messagebox.showinfo("게임 종료", "성공하였습니다")
        else:
            messagebox.showinfo("게임 종료", "실패하였습니다")

        result = messagebox.askquestion("다시 시작", "다시 시작하시겠습니까?", icon='warning')
        if result == 'no':
        	App.continue_game = 0
        	
        self.conveyor.quit()
        self.table.quit()
        self.quit()

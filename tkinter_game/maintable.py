## 수정 해야 될듯

from imagebtn import *
from tkinter import *
from random import *
import time

class Maintable(Frame):
    n = 0
    selected_image = 0
    def __init__(self, master, picture, alphabet, width):
        super(Maintable, self).__init__()
        self.image_number_list = []  # 셔플된 이미지의 번호를 저장하기 위한 리스트. 16개
        self.master = master # maintable frame의 parent 설정
        self.width = width # maintable의 넓이. = 4
        self.n = width * width # maintable에 추가될 이미지 수. = 16
        self.picture = picture # app에서 생성한 이미지 받아와서 저장

        # 숨겨진 이미지 셔플링

        self.random_shuffle()



        for i in range(0,self.width):
            for j in range(0,self.width):
                num =i*self.width+j
                w = ImageButton(self, image = alphabet[num])
                w.grid(row=i,column=j)
                w.add_hidden(alphabet=alphabet[num],hidden=picture[self.image_number_list[num]])
                w.bind("<Button-1>", self.show_hidden)
                w.bind("<ButtonRelease>", self.hide_picture)

    def random_shuffle(self):
        for i in range(16):
            randnum = randint(0, 15)
            while randnum in self.image_number_list:
                randnum = randint(0, 15)
            self.image_number_list.append(randnum)
        return self.image_number_list
        # hidden 이미지 셔플링


    # 선택된 알파벳 ImageButton의 숨겨진 이미지 출력
    def show_hidden(self, event):
        event.widget.config(image=event.widget.get_hidden())


    def hide_picture(self, event):
        time.sleep(1)
        selected_image = self.picture.index(event.widget.hidden)
        event.widget.config(image=event.widget.alphabet)
        # 카드를 알파벳이 보이게 되돌려 놓음
        if selected_image== self.master.conveyor.image_number_list[self.master.conveyor.cur_idx]:
            self.master.conveyor.correct_match()
        else:
            self.master.conveyor.wrong_match()
        # 뒤집은 카드가 찾는 카드일 경우 또는 그렇지 않을 경우의 처리

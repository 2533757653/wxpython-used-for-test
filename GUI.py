import wx
import time
import threading
from readtext import *
from readxlsx import *
import wx

class QuizFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="答题界面", size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.current_question_index = 0
        
        self.name,self.time,self.questions=readquizfile("Quiz.xlsx")
        self.create_widgets()
        
        self.Show()
        self.Maximize(True)
        
        
    def create_widgets(self):
        self.question_label = wx.StaticText(self.panel, label=self.questions[self.current_question_index]["question"])
        choices = self.questions[self.current_question_index]["choices"]
        
        self.answer_input = wx.RadioBox(self.panel, choices=choices, style=wx.VERTICAL)
        self.submit_button = wx.Button(self.panel, label="提交")
        self.before_button = wx.Button(self.panel, label="上一题")
        self.next_button = wx.Button(self.panel, label="下一题")
        self.answer=['']*len(self.questions)
        
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit_answer)
        self.before_button.Bind(wx.EVT_BUTTON,self.before)
        self.next_button.Bind(wx.EVT_BUTTON,self.next)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.submit_button, proportion=10, flag=wx.ALL, border=5)
        self.hbox.Add(self.before_button, proportion=10, flag=wx.ALL, border=5)
        self.hbox.Add(self.next_button, proportion=10, flag=wx.ALL, border=5)
        
        # 添加一个垂直间距
        self.vbox.AddSpacer(5)

        # 添加问题标签，并使其在水平方向上居中对齐
        self.vbox.Add(self.question_label, proportion=5, flag=wx.ALL|wx.EXPAND, border=5)

        # 添加一个垂直间距
        self.vbox.AddSpacer(5)

        # 添加答案选择框
        
        self.vbox.Add(self.hbox, proportion=5, flag=wx.ALL|wx.BOTTOM|wx.CENTER, border=5)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.answer_input, proportion=3, flag=wx.ALL|wx.EXPAND, border=5)
        self.panel.SetSizerAndFit(self.vbox)
        self.timer_label = wx.StaticText(self.panel, label="Time left: 0 seconds", pos=(200,200))

        self.time_to_submit = 300
        self.start_time = time.time()
        self.running = True

        self.timer_thread = threading.Thread(target=self.timer_function)
        self.timer_thread.start()

        self.Bind(wx.EVT_CLOSE, self.on_close)
    def timer_function(self):
        while self.running:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            time_left = self.time_to_submit - elapsed_time
            if time_left <= 0:
                wx.CallAfter(self.show_timeout_message)
                break
            wx.CallAfter(self.update_timer_label, time_left)
            time.sleep(1)

    def update_timer_label(self, time_left):
        time_left = max(0, int(time_left))
        self.timer_label.SetLabel(f"Time left: {time_left} seconds")

    def show_timeout_message(self):
        wx.MessageBox("Timeout! Please submit your work.", "Timeout", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_close(self, event):
        self.running = False
        if self.timer_thread:
            self.timer_thread.join()
        self.Destroy()
    def before(self,event):
        pass
    def next(self,event):
        pass 
    def submit_answer(self, event):
        # 获取用户的答案
        user_answer = self.answer_input.GetSelection() if self.questions[self.current_question_index]["type"] == "choice" else self.answer_input.GetValue()
        # 进行答案验证等逻辑
        self.answer[self.current_question_index]=user_answer
        # 显示下一题或者完成答题逻辑
        self.current_question_index += 1
        choices = self.questions[self.current_question_index]["choices"]
        if self.current_question_index < len(self.questions)-1:
            # 显示下一题
            if(self.questions[self.current_question_index]["type"]=="choice"):
                self.question_label.SetLabel(self.questions[self.current_question_index]["question"])
                self.answer_input.Destroy()
                self.answer_input=wx.RadioBox(self.panel, choices=choices, style=wx.VERTICAL)
                self.vbox.Add(self.answer_input, proportion=10, flag=wx.ALL|wx.EXPAND, border=5)
                self.vbox.Layout() 
            else:
                self.question_label.SetLabel(self.questions[self.current_question_index]["question"])
                self.answer_input.Destroy()
                self.questions[self.current_question_index]["question"]
                self.answer_input=wx.TextCtrl(self.panel)
                self.vbox.Add(self.answer_input, proportion=3, flag=wx.ALL|wx.EXPAND, border=5)
                self.vbox.Layout() 
        else:
            # 所有问题已回答完毕
            # 使用answer与self.questions作对比得出最终的答案
            print(self.answer)
            for i in range(0,len(self.answer)):
                if(self.answer[i]==0):
                    self.answer[i]="A"
                if(self.answer[i]==1):
                    self.answer[i]="B"
                if(self.answer[i]==2):
                    self.answer[i]="C"
                if(self.answer[i]==3):
                    self.answer[i]="D"
            mark=0
            for i in range(0,len(self.answer)):
                if(self.answer[i]==self.questions[i]['answer']):
                    mark+=5
            wx.MessageBox("恭喜！您已完成所有题目。\n 您的得分是"+str(mark))
            self.Close()
            self.Destroy()

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="登录", size=(400, 250))
        panel = wx.Panel(self)
        # 介绍考试的静态文本
        self.exam_intro = wx.StaticText(panel, label=readtext('小测验游戏说明.txt'))
        self.username,self.password=readxlsxfile("名单.xlsx")
        # 用户名输入框
        self.username_label = wx.StaticText(panel, label="用户名:")
        self.username_text = wx.TextCtrl(panel)
        
        
        # 密码输入框
        self.password_label = wx.StaticText(panel, label="密码:")
        self.password_text = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        
        # 登录按钮
        login_button = wx.Button(panel, label="登录")
        login_button.Bind(wx.EVT_BUTTON, self.on_login)
        
        static_box = wx.StaticBox(panel, label="小测验游戏说明")
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        static_box_sizer.Add(self.exam_intro, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.username_label, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        hbox.Add(self.username_text, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        hbox.Add(self.password_label, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        hbox.Add(self.password_text, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        hbox.Add(login_button, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        
        # 创建垂直Box布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(static_box_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        
        # 设置面板布局
        panel.SetSizerAndFit(vbox)
        self.Maximize(True)
        
    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        for i in range(0,len(self.username)):
            if(self.username[i]==username):
                break
        # 这里可以添加登录验证逻辑
        if username == self.username[i] and password == self.password[i]:
            wx.MessageBox("登录成功！", "提示", wx.OK | wx.ICON_INFORMATION)
            self.Hide()
            quiz_frame = QuizFrame()
            quiz_frame.Show()
        else:
            wx.MessageBox("ERROR","ERROR",wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()

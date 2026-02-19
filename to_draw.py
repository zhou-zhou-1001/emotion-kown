import plotly.express as px
import pandas as pd


class AllPressure:
    def __init__(self):
        self.all_pressure = {}
        self.all_date = []
        self.all_number = []
        self.date = None
        self.number = None
        self.all_the_emotion_p = []
        self.all_the_emotion_num_n = []
        self.all_the_emotion = []
        self.all_the_emotion_num = []
        self.df = pd.DataFrame(columns=('date', 'number'))
        self.the_draws = {}

    def add_all_pressure(self):
        print("压力数值不能 > 100")
        while True:
            # 输入压力数值
            self.date = input('''请写下时间，如果你好了，请用“fine”表示：''')
            print(self.date)
            if self.date == 'fine':
                break
            self.number  = input('''please write this emotion's number ,and your emotion number needs to be a int : ''')
            print(self.number)
            # 检查类型
            try:
                self.number = int(self.number)
                number = self.number

            except ValueError:
                print("please write a right number")
                continue
            if number <= 0 or  number > 100:
                print("please write a right number")
                continue

            # 存入字典
            self.all_the_emotion_p.append(self.date)
            self.all_the_emotion_num_n.append(number)



    def draw_run(self):
        self.add_all_pressure()
        df = pd.DataFrame({'date':self.all_the_emotion_p,'number': self.all_the_emotion_num_n})
        fig = px.line(df, x='date', y='number')
        fig.show()


    def draw_emotion(self ):
        self.the_draws = list(zip(self.all_the_emotion, self.all_the_emotion_num))
        # 绘制饼图
        fig = px.pie(values =self.all_the_emotion_num, names=self.all_the_emotion)
        fig.show()




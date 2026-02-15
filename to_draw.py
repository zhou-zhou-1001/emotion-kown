import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')

class AllPressure:
    def __init__(self):
        self.all_pressure = {}
        self.all_date = []
        self.all_number = []
        self.date = None
        self.number = None
        self.all_the_emotion = []
        self.all_the_emotion_num = []


    def add_all_pressure(self):
        print("the pressure number cannot > 100 ")
        while True:
            # 输入压力数值
            self.date = input('''please write the time,and if you are ok , \n use 'fine' to stand: ''')
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
            self.all_pressure[self.date]= self.number

    def turn_all_pressure(self):
        for num in self.all_pressure.values():
            self.all_number.append(num)
        for num in self.all_pressure.keys():
            self.all_date.append(num)

    def draw_run(self):

        self.add_all_pressure()
        self.turn_all_pressure()
        fig, ax = plt.subplots()
        x_num = range(1,len(self.all_date)+1 )
        ax.plot(x_num, self.all_number)
        plt.show()

    def draw_emotion(self ):
        self.all_the_emotion = []
        self.all_the_emotion_num = []
        sorted_items = sorted(self.all_emotion.items())
        self.all_the_emotion = [item[0] for item in sorted_items]
        self.all_the_emotion_num = [item[1] for item in sorted_items]

        # 绘制饼图
        plt.pie(self.all_the_emotion_num, labels=self.all_the_emotion, autopct='%1.1f%%')
        plt.title('You Emotion ')
        plt.axis('equal')
        plt.show()


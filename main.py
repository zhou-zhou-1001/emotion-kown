from to_draw import AllPressure

class Emotion (AllPressure):


    def __init__(self):
        super().__init__()
        self.objective_final_pressure = None
        self.emotion_number = None
        self.degree_num = None
        self.emotion_number_self = None
        self.emotion_x = None
        self.emotion_y = None
        self.all_emotion = {}





    def input_self_emo(self):

            # 设定总值为100
            a = 100
            print("the all emotion number add need to be 100")
            while True:
                # 输入主观情绪及数值
                self.emotion_x = input('''please write a emotion : ''')
                print(self.emotion_x)
                self.emotion_y = input(
                    '''please write this emotion's number ,and your emotion number needs to be a int : ''')
                print(self.emotion_y)

                # 检查数量是否正确
                try:
                    emotion_num = int(self.emotion_y)
                except ValueError:
                    print("please write a right number")
                    continue
                if emotion_num <= 0 or emotion_num > 100:
                    print("please write a right number")
                    continue

                if emotion_num > a:
                    print("please write a right number")
                    continue

                # 计算总值
                a = a - emotion_num

                # 存入字典

                self.all_emotion[self.emotion_x] = self.emotion_y
                self.all_the_emotion.append(self.emotion_x)
                self.all_the_emotion_num.append(emotion_num)

                if a == 0:

                    print(f'''you emotion : {self.all_emotion}''')
                    self.draw_emotion()
                    break


                else:
                    print(f"now you have {a}")


    def input_objective(self):
        while True:
            try:
                #输入主观客观压力数值及感受指数
                emotion_number_input_self = input(
                    "Enter your pressure  emotion number,and your  emotion number needs to be a int : ")
                self.emotion_number_self = int(emotion_number_input_self)

                degree_num_input = input("Enter your degree number,and your degree number needs to be a float : ")
                self.degree_num = float(degree_num_input)

                emotion_number_input = input(
                    "Enter your pressure objective emotion number,and your objective emotion number needs to be a int : ")
                self.emotion_number = int(emotion_number_input)

                #检查数值
                if 0 <= self.emotion_number <= 100 and 0 <= self.emotion_number_self <= 100 and 0 <= self.emotion_number <= 100:
                    print("this is a right number")
                else :
                    print("please write a right number")

                if 0 <= self.degree_num <= 1:
                    print("this is a right number")
                else:
                    print("please write a right number")

                #计算结果
                self.objective_final_pressure = self.emotion_number * self.degree_num
                final = (self.emotion_number_self + self.objective_final_pressure) / 2
                print(f"your final pressure emotion is {final}")
                break
            except ValueError:
                print("please write a right number")

    #执行程序
    def start(self):
        while True:
            ask = input("if  you want to draw the all date pressure ,add '1',\n"
                        "if you want to see all you emotion,add '2',\n"
                        " if you want to see your finish pressure number ,add '3'\n"
                        "if you want to out,add 'out'\n")
            print(ask)
            if ask == '1':
                self.draw_run()
                continue
            elif ask == '2':
                self.input_self_emo()
                continue
            elif ask == '3':
                self.input_objective()
                continue

            elif ask == 'out':
                print("ok")
                break

            else:
                print("please write a right number")
                continue


#初始化
emotion = Emotion()
#执行
emotion.start()


from to_draw import AllPressure
from suggestion import suggestion
import sqlite3
conn = sqlite3.connect('emotion.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS emotion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')
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
            print("所有的情绪数值总和需为100")
            while True:
                # 输入主观情绪及数值
                self.emotion_x = input('''请写下一个情绪''')
                print(self.emotion_x)
                self.emotion_y = input(
                    '''请写下这个情绪的数值为几，并且这个数值需要为一个整数''')
                print(self.emotion_y)

                # 检查数量是否正确
                try:
                    emotion_num = int(self.emotion_y)
                except ValueError:
                    print("请写上正确的数值")
                    continue
                if emotion_num <= 0 or emotion_num > 100:
                    print("请写上正确的数值")
                    continue

                if emotion_num > a:
                    print("请写上正确的数值")
                    continue

                # 计算总值
                a = a - emotion_num

                # 存入字典

                self.all_emotion[self.emotion_x] = self.emotion_y
                self.all_the_emotion.append(self.emotion_x)
                self.all_the_emotion_num.append(emotion_num)

                if a == 0:

                    print(f'''你的情绪由 : {self.all_emotion} 组成''')
                    self.draw_emotion()
                    break


                else:
                    print(f"现在你还有 {a} 的情绪数值剩余量")


    def input_objective(self):
        while True:
            try:
                #输入主观客观压力数值及感受指数
                emotion_number_input_self = input(
                    " 输入你的压力情绪数值，且你的情绪数值需要为整数。")
                self.emotion_number_self = int(emotion_number_input_self)

                degree_num_input = input("输入你的感受程度，且这个数值在0到2之间，需要是一个小数：")
                self.degree_num = float(degree_num_input)

                emotion_number_input = input(
                    " 输入你的压力客观情绪数值，且你的客观情绪数值必须为整数：")
                self.emotion_number = int(emotion_number_input)

                #检查数值
                if 0 <= self.emotion_number <= 100 and 0 <= self.emotion_number_self <= 100 and 0 <= self.emotion_number <= 100:
                    print("这是正确的格式数字")
                else :
                    print("请写上正确的数值")

                if 0 <= self.degree_num <= 2:
                    print("这是正确的格式数字")
                else:
                    print("请写上正确的数值")

                #计算结果
                self.objective_final_pressure = self.emotion_number * self.degree_num
                final = (self.emotion_number_self + self.objective_final_pressure) / 2
                print(f"你最终的压力数值为 {final}")
                suggestion(final)

                break
            except ValueError:
                print("请写上正确的数值")

    def write(self):
        time = input('请输入事件日期（格式：YYYY-MM-DD,例如2026-01-01')
        print(time)
        thing = input('请输入你想记录的事件')
        print(thing)
        c.execute("INSERT INTO emotion (date,content)VALUES (?,?)",
                  (time, thing))
        conn.commit()
        conn.close()
        print(f"事件已保存")

    def see_all_thing(self):
        conn = sqlite3.connect('emotion.db')
        c = conn.cursor()
        print("正在查询您的学习笔记...")
        c.execute("SELECT * FROM emotion")
        all_notes = c.fetchall()
        if len(all_notes) == 0:
            print("记录是空的，快去添加一条吧！")
        else:
            print(f"共找到 {len(all_notes)} 条笔记：")
            for note in all_notes:
                print(f"ID:{note[0]} | 日期:{note[1]}")
                print(f"内容:{note[2]}")
        conn.close()

    #执行程序
    def start(self):
        while True:
            ask = input("如果你想绘制所有日期的压力值，输入'1'，\n"
            "如果你想查看所有情绪记录，输入'2'，\n"
            "如果你想查看最终压力数值，输入'3'，\n"
            "如果你想记录事件，输入'4'\n"
            "如果你想查看事件，输入'5'\n"
            "如果你想退出，输入' out'\n"
            '-------------------------------------------------------------------------------\n')
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

            elif ask == '4':
                self.write()
                continue

            elif ask == '5':
                self.see_all_thing()
                continue

            elif ask == 'out':
                print("已完成")
                break

            else:
                print("请输入正确的数字")
                continue




#初始化
emotion = Emotion()
#执行
emotion.start()


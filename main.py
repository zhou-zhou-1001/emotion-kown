from to_draw import AllPressure
from suggestion import suggestion
import sqlite3

conn_thing = sqlite3.connect('thing.db')
c_thing = conn_thing.cursor()
conn_emo = sqlite3.connect('all_emotion_record.db')
c_emo = conn_emo.cursor()
c_thing.execute('''
                CREATE TABLE IF NOT EXISTS thing
                (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    date    TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                ''')
conn_thing.commit()
c_emo.execute('''
              CREATE TABLE IF NOT EXISTS all_emotion_record
              (
                  id          INTEGER PRIMARY KEY AUTOINCREMENT,
                  date        TEXT NOT NULL,
                  all_emotion TEXT NOT NULL
              )
              ''')
conn_emo.commit()

class Emotion(AllPressure):

    def __init__(self):
        super().__init__()
        self.all_notes = None
        self.objective_final_pressure = None
        self.emotion_number = None
        self.degree_num = None
        self.emotion_number_self = None
        self.emotion_x = None
        self.emotion_y = None
        self.all_emotion = {}
        self.c_thing = c_thing
        self.conn_thing = conn_thing
        self.c_emo = c_emo
        self.conn_emo = conn_emo
        self.emo_date = None
        self.all_the_emotion = []
        self.all_the_emotion_num = []

    def input_self_emo(self):

        # 设定总值为100
        a = 100
        print("所有的情绪数值总和需为100")
        emo_date = input('请输入事件日期（格式：YYYY-MM-DD,例如2026-01-01')

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

            self.all_emotion[self.emotion_x] = emotion_num
            self.all_the_emotion.append(self.emotion_x)
            self.all_the_emotion_num.append(emotion_num)

            if a == 0:

                print(f'''你的情绪由 : {self.all_emotion} 组成''')
                self.draw_emotion()
                choice_all_emotion = input("是否保存此分析？是按' yes',不是按'no'")
                if choice_all_emotion == 'yes':
                    all_emotion_str = str(self.all_emotion)
                    # noinspection SqlResolve
                    self.c_emo.execute("INSERT INTO all_emotion_record (date,all_emotion)VALUES (?,?)",
                                       (emo_date, all_emotion_str))
                    self.conn_emo.commit()

                    print(f"事件已保存")

                break


            else:
                print(f"现在你还有 {a} 的情绪数值剩余量")

    def see_all_emo_thing(self):

        print("正在查询您的情绪分析记录...")
        # noinspection SqlResolve
        self.c_emo.execute("SELECT * FROM all_emotion_record")
        all_notes = self.c_emo.fetchall()
        if len(all_notes) == 0:
            print("记录是空的，快去添加一条吧！")
        else:
            print(f"共找到 {len(all_notes)} 条记录：")
            for note in all_notes:
                print(f"ID:{note[0]} | 日期:{note[1]}")
                print(f"内容:{note[2]}")

    def input_objective(self):
        while True:
            try:
                # 输入主观客观压力数值及感受指数
                emotion_number_input_self = input(
                    " 输入你的压力情绪数值，且你的情绪数值需要为整数。")
                self.emotion_number_self = int(emotion_number_input_self)

                degree_num_input = input("输入你的感受程度，且这个数值在0到2之间，需要是一个小数：")
                self.degree_num = float(degree_num_input)

                emotion_number_input = input(
                    " 输入你的压力客观情绪数值，且你的客观情绪数值必须为整数：")
                self.emotion_number = int(emotion_number_input)

                # 检查数值
                if 0 <= self.emotion_number <= 100 and 0 <= self.emotion_number_self <= 100 and 0 <= self.emotion_number <= 100:
                    print("这是正确的格式数字")
                else:
                    print("请写上正确的数值")

                if 0 <= self.degree_num <= 2:
                    print("这是正确的格式数字")
                else:
                    print("请写上正确的数值")

                # 计算结果
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
        # noinspection SqlResolve
        self.c_thing.execute("INSERT INTO thing (date,content)VALUES (?,?)",
                             (time, thing))
        self.conn_thing.commit()

        print(f"事件已保存")

    def see_all_thing(self):
        print("正在查询您的事件记录...")
        # noinspection SqlResolve
        self.c_thing.execute("SELECT * FROM thing")
        self.all_notes = self.c_thing.fetchall()
        if len(self.all_notes) == 0:
            print("记录是空的，快去添加一条吧！")
        else:
            print(f"共找到 {len(self.all_notes)} 个事件：")
            for note in self.all_notes:
                print(f"ID:{note[0]} | 日期:{note[1]}")
                print(f"内容:{note[2]}")

    # 执行程序
    def start(self):
        while True:
            ask = input("如果你想绘制所有日期的压力值，输入'1'，\n"
                        "如果你想查看所有情绪记录，输入'2'，\n"
                        "如果你想查看最终压力数值，输入'3'，\n"
                        "如果你想记录事件，输入'4'\n"
                        "如果你想查看事件，输入'5'\n"
                        "如果你想查看情绪分析记录，输入'6'\n"
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

            elif ask == '6':
                self.see_all_emo_thing()
                continue

            elif ask == 'out':
                print("已完成")
                break

            else:
                print("请输入正确的数字")
                continue


# 初始化
emotion = Emotion()
# 执行
emotion.start()
conn_emo.close()
conn_thing.close()
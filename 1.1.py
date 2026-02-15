class Emotion :


    def __init__(self,happy,sad,anger,fear,unknown ):
        self.happy = happy
        self.sad = sad
        self.anger = anger
        self.fear = fear
        self.unknown = unknown


    def input(self):
        return [self.happy,self.sad,self.anger,self.fear,self.unknown]


emotion = Emotion('happy','sad','anger','fear','unknow')

emotion_number = 0
emotion_num = 0
emo_v =[]


print("the all emotion number add need to be 10")
for a in emotion.input():
    while True:
        try:
            emotion_num = input(f"Enter you {a} number,and your emotion number needs to be a int: ")
            emotion_num = int(emotion_num)
            emo_v.append(emotion_num)
            break
        except ValueError:
            print("please write a right number")


while True:
    try:
        degree_num = input("Enter your degree number,and your degree number needs to be a float : ")
        float(degree_num)
        degree_num = float(degree_num)
        if degree_num <= 1:
           break
        else:
            print("please write a right number")
    except ValueError:
        print("please write a right number")

num = len(emotion.input())
emo_all = sum(emo_v)
this_num = 0
int(emo_all)
final = emo_all * degree_num
print(f"your this emotion is {final}")
















import plotly.express as px
import streamlit as st
import pandas as pd
import sqlite3
import datetime as dt


st.set_page_config(
    page_title="Emotion Know",
    layout="wide",
)

st.title("Emotion Know")
st.markdown("---")


#侧边栏导航
st.sidebar.title( "菜单栏")

#初始化
@st.cache_resource
def init_db():

     """初始化数据库连接和表结构"""
     # 连接事件数据库
     conn_thing = sqlite3.connect('thing.db', check_same_thread=False)
     c_thing = conn_thing.cursor()

     # 创建事件表（如果不存在）
     c_thing.execute('''
        CREATE TABLE IF NOT EXISTS thing
        (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            date    TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
     conn_thing.commit()
     # 连接情绪数据库
     conn_emo = sqlite3.connect('all_emotion_record.db', check_same_thread=False)
     c_emo = conn_emo.cursor()

     # 创建情绪记录表（如果不存在）
     c_emo.execute('''
        CREATE TABLE IF NOT EXISTS all_emotion_record
        (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            date    TEXT NOT NULL,
            all_emotion TEXT NOT NULL
        )
    ''')
     conn_emo.commit()
     return conn_thing, c_thing, conn_emo, c_emo
conn_thing, c_thing, conn_emo, c_emo = init_db()

st.sidebar.success( "连接成功")
st.write("你好，这里是“Emotion Know")

#功能展示
st.subheader("功能预览")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric( "功能块" , "6个" , "完整")

with col2:
    st.metric( "数据库" , "2个" ,"已连接")

with col3:
    st.metric( "状态" , "就绪"  ,"运行中")


#事件记录
st.markdown("## 事件记录功能")

tab1,tab2 = st.tabs( ["记录新事件" , "查看所有事件"])
with tab1:
    st.subheader( "添加事件记录")
    with st.form ( "event_from") :
        event_date = st.date_input("选择日期",value=pd.Timestamp.now())
        event_content = st.text_area("事件内容",
                                         placeholder= "请输入你想记录的事件",
                                         height = 150)
        submitted = st.form_submit_button("保存事件")

        if submitted:
            if event_content.strip():
                c_thing.execute("INSERT INTO thing (date,content)VALUES (?,?)",
                                    (event_date.strftime("%Y-%m-%d"), event_content))
                conn_thing.commit()
                st.success(f"事件已保存，日期：{event_date}")
                st.balloons()

            else:
                st.warning( " 请输入事件内容 ")
#查询事件
with tab2 :
    st.subheader("所有事件记录")

    if st.button( "刷新记录",key = "refresh_events"):
        st.rerun()

    c_thing.execute("SELECT * FROM thing")
    all_notes = c_thing.fetchall()
    if len(all_notes) == 0:
        st.info("记录是空的，快去添加一条吧！")
    else:
        st.success(f"共找到 {len(all_notes)} 个事件：")
        events_df = pd.DataFrame(all_notes, columns=['ID', '日期', '内容'])
        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True,
            column_config= {
                "ID": st.column_config.NumberColumn("ID",width= "small"),
                "日期":st.column_config.DateColumn("日期"),
                "内容" : st.column_config.TextColumn("内容",width= "large")
            }
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总记录数",len(all_notes))
        with col2:
            if len(all_notes) > 0:
                recent_date = events_df['日期'].iloc[0]
                st.metric("最近记录",recent_date)




st.markdown("---")
st.markdown("情绪组成分析")
emo_tab1, emo_tab2 = st.tabs(["情绪组成", "情绪记录"])
with emo_tab1:
    st.subheader("分析你的情绪组成")
    st.info("所有的情绪数值总和需为100")

    emotion_date = st.date_input("选择日期",
                                 value=pd.Timestamp.now(),
                                 key="emo_date_input")
    st.markdown("### 添加情绪")

    if 'emotion_dict' not in st.session_state:
        st.session_state.emotion_dict = {}
    if 'total_remaining' not in st.session_state:
        st.session_state.total_remaining = 100
    if 'emotion_list' not in st.session_state:
        st.session_state.emotion_list = []
    if 'emotion_value_list' not in st.session_state:
        st.session_state.emotion_value_list = []

    remaining = int(st.session_state.total_remaining)
    st.markdown(f"**剩余分配情绪数值为：{remaining}/100**")


    with st.form(key="add_form",clear_on_submit=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            emotion_name = st.text_input("情绪名称",
                                         placeholder="如开心，焦虑...",
                                         key="emotion_name")

        with col2:
            max_val = min(remaining, 100)
            emotion_value = st.number_input("情绪数值",
                                            min_value=1,
                                            max_value=max_val if max_val > 0 else 1,
                                            value=1 if remaining >= 1 else 1,
                                            step=1,
                                            key="emotion_value")

        add_button = st.form_submit_button("添加此情绪")

    if add_button:
        if emotion_name.strip():
            if emotion_value <= remaining:
                st.session_state.emotion_dict[emotion_name] = emotion_value
                st.session_state.emotion_list.append(emotion_name)
                st.session_state.emotion_value_list.append(emotion_value)
                st.session_state.total_remaining -= emotion_value

                st.success(f"添加了情绪{emotion_name}({emotion_value})")
                st.rerun()

            else:
                st.error(f"值过大，最大只能添加{remaining}")

        else:
            st.warning("请输入情绪名称")

    if st.session_state.emotion_dict:
        st.markdown("### 已添加的情绪")

        cols = st.columns(3)
        for idx, (emotion_name, emotion_value) in enumerate(st.session_state.emotion_dict.items()):
            with cols[idx % 3]:
                st.metric(
                    label=f"{emotion_name}",
                    value=emotion_value, )

    st.markdown("---")
    if st.session_state.total_remaining == 0:
        st.success("完成")

        with st.form(key="emotion_form"):
            st.write("你的情绪组成：", st.session_state.emotion_dict)
            complete_button = st.form_submit_button("保存并完成")



        if complete_button:
            try:
                all_emotion_str = str(st.session_state.emotion_dict)
                c_emo.execute("INSERT INTO all_emotion_record (date, all_emotion) VALUES (?, ?)",
                                  (emotion_date.strftime("%Y-%m-%d"), all_emotion_str))
                conn_emo.commit()
                st.balloons()
                st.success("保存成功")
                st.markdown("情绪分布饼图")
                emotion_names = list(st.session_state.emotion_dict.keys())
                emotion_values = list(st.session_state.emotion_dict.values())

                if emotion_names and emotion_values:
                    fig = px.pie(
                        values=emotion_values,
                        names=emotion_names,
                        title=f"情绪分布 - {emotion_date}",
                    )

                fig.update_layout(
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

                st.session_state.emotion_dict = {}
                st.session_state.total_remaining = 100
                st.session_state.emotion_list = []
                st.session_state.emotion_value_list = []

                st.rerun()

            except Exception as e:
                st.error(f"保存失败：{str(e)}")

    elif 0 < st.session_state.total_remaining < 100:
            remaining = st.session_state.total_remaining
            st.error(f"请继续添加程序，剩余{remaining}未分配")

            if st.button("重新开始") :
                st.session_state.emotion_dict = {}
                st.session_state.total_remaining = 100
                st.session_state.emotion_list = []
                st.session_state.emotion_value_list = []
                st.success("已清空")

                st.rerun()

with emo_tab2 :
    st.subheader("所有情绪分析记录")

    if st.button( "刷新记录",key = "refresh_emotion"):
        st.rerun()

    c_emo.execute("SELECT * FROM all_emotion_record")
    all_emotion = c_emo.fetchall()
    if len(all_emotion) == 0:
        st.info("情绪分析记录是空的，快去添加一条吧！")
    else:
        st.success(f"共找到 {len(all_emotion)} 个事件：")
        emotions_df = pd.DataFrame(all_emotion, columns=['ID', '日期', '内容'])
        st.dataframe(
            emotions_df,
            use_container_width=True,
            hide_index=True,
            column_config= {
                "ID": st.column_config.NumberColumn("ID",width= "small"),
                "日期":st.column_config.DateColumn("日期"),
                "情绪分析" : st.column_config.TextColumn("情绪分析",width= "large")
            }
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总记录数",len(all_emotion))
        with col2:
            if len(all_emotion) > 0:
                recent_date = events_df['日期'].iloc[0]
                st.metric("最近记录",recent_date)

        st.markdown("---")
        st.markdown("### 详细记录")

        for record in all_emotion:
            record_id = record[0]
            record_date = record[1]
            record_emotion = record[2]

            with st.expander(f" 日期 ： {record} - 记录ID ：{record_id}"):
                st.write(f"**记录日期：** {record_date}")
                st.write(f"**记录ID：** {record_id}")

                try :
                    emotion_dict = eval(record_emotion)
                    st.write("**饼图展示：**")
                    emotion_names = list(emotion_dict.keys())
                    emotion_values = list(emotion_dict.values())

                    fig = px.pie(
                        values=emotion_values,
                        names=emotion_names,
                        title=f"情绪分布 - {record_date}",
                    )

                    fig.update_layout(
                        height = 300,
                        showlegend=True,
                    )

                    st.plotly_chart(fig, use_container_width=True)

                except :
                    st.write("解析失败")

                col_btn1, col_btn2 = st.columns([1,3])
                with col_btn1:
                    if st.button( "删除",key = f"delete_{record_id}"):
                        c_emo.execute("DELETE FROM all_emotion_record WHERE ID=?",(record_id,))
                        conn_emo.commit()
                        st.success("记录已删除")
                        st.rerun()





st.markdown("---")
st.markdown("## 压力计算")

pressure_tab1 = st.tabs(["计算压力值"])[0]

with pressure_tab1 :
    st.subheader("计算你的压力值")
    st.info("""
    计算说明：
    1.主观压力 ： 你感受到的压力（0～100）
    2. 客观压力： 生理数据经计算的压力（0～100）
    3. 感受程度： 压力对你的影响程度（0～2）
    """)

    with st.form(key="pressure_form"):
        st.write("### 请输入以下数值： ")

        col1, col2,col3 = st.columns(3)
        with col1:
            emotion_number_self =st.number_input(
                "主观压力值",
                min_value=0,
                max_value=100,
                value=50,
                help = "你自己感到的压力程度（0～100）"
            )

        with col2:
            emotion_number =st.number_input(
                "客观压力值",
                min_value=0,
                max_value=100,
                value=50,
                help="生理数据体现的压力程度（0～100）"
            )

        with col3:
            degree_number =st.number_input(
                "感受程度",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                help="压力对你的影响（0～2）"
            )

        match_button = st.form_submit_button("计算压力值")
        if match_button:
            try:
                objective_final_pressure = emotion_number * degree_number
                final = (emotion_number_self + objective_final_pressure) / 2
                st.success(f"经计算 ，你的最终压力值为 {final}")

                st.markdown("建议")
                if final <= 30:
                    st.success('你现在的压力值为轻度，多多保持，记得天天开心')

                elif 30 < final <= 70:
                    st.success('你现在的压力值中等，可以休息一会')

                elif 70 < final <= 100:
                    st.success('你现在的压力值较高，建议停下手中的事，深呼吸，听一段纯音乐')

            except Exception as e:
                st.error(f"计算出错：{str(e)}")














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







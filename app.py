import streamlit as st
import random
import json
import time

from PIL import Image
import major

# 例如
# "S/N": [ {"question": "我喜欢按部就班地解决问题，而不是寻找全新的方法。", "score": "S"}, ...]
# 用户的选择的数值将加在"S"上
# 从文件加载问题

mbti_dims = ['EI', 'SN', 'TF', 'JP']

@st.cache_data
def generate_questions():
    with open('questions.json', 'r') as file:
        all_questions = json.load(file)
    return {dim: random.sample(all_questions[dim], 5) for dim in mbti_dims}

# 随机生成新的题库
questions = generate_questions()

# 用户答案计分板
if "user_score" not in st.session_state:
    st.session_state.user_score = {
        "EI": [0, -0.1],  # 外向(E)与内向(I)
        "SN": [0, -0.1],  # 感觉(S)与直觉(N)
        "TF": [0, -0.1],  # 思考(T)与情感(F)
        "JP": [0, -0.1]   # 判断(J)与知觉(P)
    }


def page0():
    introduce_test = """
> MBTI基于卡尔·荣格的心理学理论，将人格划分为16种不同类型。
> 
> 每种类型由四个维度表示：

类型   | 标识 | 描述     
------|------|----------
外向（Extraversion） | E  | 喜欢与他人互动，从外部环境中获取能量。
内向（Introversion） | I  | 喜欢独处，从内部世界中获取能量。
 | | 
感觉（Sensing）   | S  | 注重具体细节和现实情况，倾向于实用和现实。
直觉（Intuition） | N  | 注重抽象概念和未来可能性，倾向于想象和探索。
 | | 
思考（Thinking） | T  | 以逻辑和客观的方式做决策，注重事实和原则。
情感（Feeling）  | F  | 以情感和价值观为基础做决策，注重他人感受和关系。
 | | 
判断（Judging）    | J  | 喜欢有结构和组织，倾向于计划和控制。
知觉（Perceiving） | P  | 喜欢灵活应对，倾向于适应和探索。

> 在这个测试中，您将回答一系列关于自己偏好和行为方式的问题。
>
> 请尽量根据您的真实感受和反应回答问题。
>
> **没有正确或错误的答案**，只有反映您个人倾向的选项。
>
> 完成测试后，您将获得一个MBTI人格类型代码，例如"INFJ"或"ESTP"。
>
> 这个代码将帮助您更好地理解自己的偏好和特点，并为个人发展和职业选择提供有价值的参考。


#
##### 准备好了吗？开始探索自己吧!

    """
    st.markdown(introduce_test)
    if st.button("开始"):
        st.session_state.page = 1
        st.experimental_rerun()


#构造page1到page4
def create_page_function(number):
    dim = mbti_dims[number-1]
    def page_function():
        st.markdown(f"## 进度{number}/4")
        st.markdown("""
>  最左侧[-3]表示"非常不认同"    最右侧[3]表示"非常认同"
> 
>  如果不确定,则保持在中间[0]。
                    """)

        for q in questions[dim]:
            answer = st.slider(q["question"], min_value=-3, max_value=3, value=0, step=1)
            index = dim.index(q["score"])
            st.session_state.user_score[dim][index] += answer

        if st.button("下一步"):
            st.session_state.page += 1
            st.experimental_rerun()
    return page_function

for i in range(1, 4+1):
    page_func = create_page_function(i)
    globals()[f"page{i}"] = page_func

# 结果page
def page5():
    personality_type = "".join([dim[0] if st.session_state.user_score[dim][0] > st.session_state.user_score[dim][1] else dim[1] for dim in mbti_dims])
    st.markdown("### 你的MBTI类型可能是:")
    st.markdown(f"# {personality_type}")
    # st.markdown(f"<p style='color:red'>{personality_type}</p>",True) # HTML


    st.markdown("---")
    st.markdown("现在,随便介绍一下自己,让AI结合你的类型,来帮助你选择专业")
    # 用户选择性别
    gender = st.radio('选择你的性别', ('男', '女'), horizontal=True)
    # 用户选择理科/文科
    subject = st.radio('你学的是文科还是理科', ('理科', '文科'), horizontal=True)
    # 用户输入自我介绍
    evaluation = st.text_input('请随便介绍一下自己')

    # 整理用户信息为 json
    user_info = {
        "gender": gender,        # 性别
        "subject": subject,      # 文理科
        "MBTI": personality_type,  # MBTI
        "evaluation": evaluation  # 自我评价
    }

    if st.button("AI计算"):
        st.session_state.page += 1
        st.session_state.user_info = user_info
        st.experimental_rerun()

def page6():
    # import major
    # 显示进度条
    my_bar = st.progress(0, "AI开始计算...")
    my_bar.progress(2,"正在检索中国大学专业数据库...")
    time.sleep(1)
    my_bar.progress(20, "正在检索中国大学专业数据库...")
    time.sleep(1)
    my_bar.progress(31, "正在匹配信息(此过程较长)...")
    result = major.main(st.session_state.user_info)
    time.sleep(1)
    my_bar.progress(81, "使用GPT4进行精确匹配...")
    st.markdown(f"# AI根据你的信息分析结果:")
    time.sleep(1)
    my_bar.progress(100, "完成")
    st.markdown(f"{result}")

    # 渲染result
    # 这里我只是简单的显示了结果，你可能需要根据result的结构来定制你的显示方式
    # st.write(result)
    # st.markdown(f"{result.personality_type}")
    # st.markdown(f"{result.suggestion}")

    
    # st.markdown("## 5个专业推荐:")

    # for each in result.major5:
    #     st.markdown("---")
    #     st.markdown("## 专业{each.index}")
    #     st.markdown("## {each.major}:")
    #     st.markdown("## {each.details.top5}:")
    #     st.markdown("## {each.details.good5}:")
    #     st.markdown("## {each.details.institutions}:")
    #     st.markdown("## {each.details.jobtitle}:")
    #     st.markdown("---")

image = Image.open('./static/aiteam.png')
st.sidebar.image(image, caption='AI小分队', use_column_width=True)

st.title(":star: AI选专业")

if "page" not in st.session_state:
    st.session_state.page = 0

if st.session_state.page == 1: 
    page1()
elif st.session_state.page == 2: 
    page2()
elif st.session_state.page == 3: 
    page3()
elif st.session_state.page == 4: 
    page4()
elif st.session_state.page == 5: 
    page5()
elif st.session_state.page == 6: 
    page6()
else:
    page0()


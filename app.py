import streamlit as st
import random
import json
import time
from datetime import datetime

from PIL import Image
import major
import invitation

# 例如
# "S/N": [ {"question": "我喜欢按部就班地解决问题，而不是寻找全新的方法。", "score": "S"}, ...]
# 用户的选择的数值将加在"S"上
# 从文件加载问题

st.set_page_config(page_title="AI选专业(@AI小分队)")

def save_history(user_info):
    current_date = datetime.now().strftime("%Y%m%d")
    path = "./static/history.json"

    # 将字典转换为JSON字符串
    json_str = json.dumps(user_info)

    # 打开文件并将数据写入
    with open(path, "a", encoding="utf-8") as file:
        json.dump({current_date: user_info}, file, ensure_ascii=False)
        file.write("\n")

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
        > 这个测试基于卡尔·荣格的心理学理论，**没有正确或错误的答案**，只反映您个人倾向。
        >
        > 完成测试后，你将获得一个人格类型代码，例如"INFJ"或"ESTP"。
        >
        > 这个代码将帮助您更好地理解自己的偏好和特点，并为个人发展和职业选择提供参考。
        #
        ##### 准备好了吗？开始探索自己吧!
    """

    st.warning("""
        选专业，相对于高考来说，甚至是更重要的一件事情。
       
        要想在800个专业里，几乎不可能选到最适合自己的。
       
        还好我们现在有了AI，可以给我们一些建议。
    """)
    st.markdown(introduce_test)
    user_code = st.text_input("请输入邀请码")
    if st.button("开始"):
        invitation_codes = invitation.load_invitation_codes()
        if user_code in invitation_codes:  # 检查用户输入的邀请码是否正确
            st.session_state.page = 1
            st.experimental_rerun()
        else:
            st.warning("请输入正确的邀请码")


#构造page1到page4
def create_page_function(number):
    dim = mbti_dims[number-1]
    def page_function():
        if number == 1:
            jindu = "◉○○○"
        elif number == 2:
            jindu = "◉◉○○ "
        elif number == 3:
            jindu = "◉◉◉○ "
        elif number == 4:
            jindu = "◉◉◉◉"
        else:
            jindu = "◉◉◉◉"
        st.markdown(f"""
                    >  进度: {jindu}
                    > 
                    >  根据对这句话的**认可度**选择
                    ---
                    """)
        for q in questions[dim]:
            transdict = {
                "非常不认同": -3,
                "不认同": -2,
                "应该不是": -1,
                "不确定": 0,
                "应该是": 1,
                "认同": 2,
                "非常认同": 3
            }
            user_selector = st.select_slider(q["question"], ("非常不认同","不认同","应该不是","不确定","应该是","认同","非常认同"), "不确定")
            st.markdown("---")
            answer = transdict[user_selector]
            index = dim.index(q["score"])
            st.session_state.user_score[dim][index] += answer
        st.markdown(f"""
                    >  进度: {jindu}
                    ---
                    """)

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
    st.markdown("## 你的性格类型可能是:")
    st.markdown(f"# :point_right: {personality_type}")
    # st.markdown(f"<p style='color:red'>{personality_type}</p>",True) # HTML


    st.markdown("---")
    st.markdown("现在,随便介绍一下自己,让AI结合你的类型,来帮助你选择专业")
    # 用户选择性别
    gender = st.radio('选择你的性别', ('男👦', '女👧'), horizontal=True)
    # 用户选择理科/文科
    subject = st.radio('你学的是文科还是理科', ('理科', '文科'), horizontal=True)
    # 用户输入自我介绍

    # evaluation = st.text_area('请随便介绍一下自己')
    evaluation = st.text_area('请随便介绍一下自己,让AI更了解你', value="比如:我喜欢打游戏 / 我的梦想是... / 这辈子不可能打工 / 数学不行 / 英语很好 / 比较宅 / 喜欢旅行")

    # if st.button("AI推荐"):
    #     st.cache_data.clear()
    #     st.session_state.page = 6
    #     st.session_state.user_info = user_info
    #     st.experimental_rerun()

    if len(evaluation) > 10:
        # 整理用户信息为 json
        user_info = {
            "gender": gender,          # 性别
            "subject": subject,        # 高考是文科或理科
            "mbti": personality_type,  # MBTI类型
            "evaluation": evaluation,   # 自我评价
            "major5": []               # 推荐的专业
        }
        if st.button("AI推荐"):
            st.cache_data.clear()
            st.session_state.page = 6
            st.session_state.user_info = user_info
            st.experimental_rerun()
    else:
        st.write("请输入至少10个字符")

def page6():
    # import major
    # 显示进度条
    my_bar = st.progress(0, ":fire: AI开始计算...")
    time.sleep(1)
    my_bar.progress(5,":books: 正在整理数据...")

    while True:
        try:
            st.session_state.user_info = major.add_major(st.session_state.user_info)
            break  # 如果成功执行，跳出循环
        except Exception as e:
            st.error("服务器过载，正在重新计算")
            continue  # 继续重新执行该代码段

    save_history(st.session_state.user_info)
    my_bar.progress(21,":mag: 正在检索中国大学专业数据库...")
    st.markdown(f"# :zap: AI分析结果:")

    while True:
        try:
            result1 = major.analysis_mbti(st.session_state.user_info)
            break  # 如果成功执行，跳出循环
        except Exception as e:
            st.error("服务器过载，正在重新计算")
            continue  # 继续重新执行该代码段
    my_bar.progress(51, ":rocket: 正在匹配合适的专业...")
    st.markdown(f"{result1}")
    st.markdown("---")

    while True:
        try:
            result2 = major.why_major5(st.session_state.user_info)
            break  # 如果成功执行，跳出循环
        except Exception as e:
            st.error("服务器过载，正在重新计算")
            continue  # 继续重新执行该代码段
    my_bar.progress(81, ":tea: 正在整理结果...")
    st.markdown(f"{result2}")
    st.markdown("---")

    while True:
        try:
            result3 = major.analysis_major5(st.session_state.user_info)
            break  # 如果成功执行，跳出循环
        except Exception as e:
            st.error(" :grey_exclamation: 服务器过载，正在重新计算")
            continue  # 继续重新执行该代码段
    my_bar.progress(100, ":bulb: 完成")
    st.markdown(f"{result3}")
    st.markdown("---")

    new_code = str(random.randint(1000, 9999))  # 生成一个新的四位数邀请码
    st.markdown("> 解锁了新的邀请码，可以邀请朋友来体验:")
    st.markdown(f"# :point_right: {new_code}")
    st.markdown("> https://zhuanye.aiis.run")
    st.markdown("> 关注@AI小分队")
    qun_image = Image.open('./static/qun.png')
    st.image(qun_image, caption='志愿报考交流群', use_column_width=True)
    invitation.save_invitation_code(new_code)

# 设置sidebar
side_image = Image.open('./static/aiteam.png')
st.sidebar.image(side_image, caption='@AI小分队', use_column_width=True)
st.sidebar.markdown("因算力有限，项目未公开")
st.sidebar.markdown("抖音@AI小分队 **获取邀请码**进行体验")
st.sidebar.markdown("完成后会获得邀请码，可以邀请朋友体验")
st.sidebar.markdown("#### 此测试完全免费:exclamation:")

#页面标题
st.title(":star: AI选专业")
st.markdown("---")

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


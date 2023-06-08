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

personality_dict = {
    "ISTJ": {"style": "物流师型人格","good":"实际且注重事实的个人，可靠性不容怀疑。", "major": ["会计", "保险规划师", "证券分析员", "档案管理员", "工程技术人员", "农学家", "地质学家"]},
    "ISFJ": {"style": "守卫者型人格","good":"非常专注而温暖的守护者，时刻准备着保护爱着的人们。", "major": ["护士医师", "教师", "社工", "营养师", "图书管理员", "公益机构人员", "项目经理", "旅馆负责人"]},
    "INFJ": {"style": "提倡者型人格","good":"安静而神秘，同时鼓舞人心且不知疲倦的理想主义者", "major": ["心理咨询师", "作家", "培训师", "职业规划师", "文字编辑", "律师", "艺术指导", "市场营销人员"]},
    "INTJ": {"style": "建筑师型人格","good":"富有想象力和战略性的思想家，一切皆在计划之中。", "major": ["经济学者", "科学家", "程序员", "证券投资分析师", "财务专家", "律师"]},
    "ISTP": {"style": "鉴赏家型人格","good":"大胆而实际的实验家，擅长使用任何形式的工具。", "major": ["程序员", "警察", "消防员", "证券分析师", "数据分析师", "药剂师", "银行职员"]},
    "ISFP": {"style": "探险家型人格","good":"灵活有魅力的艺术家，时刻准备着探索和体验新鲜事物。", "major": ["歌手", "画家", "设计师", "厨师", "园艺设计师", "商人", "销售经理"]},
    "INFP": {"style": "调停者型人格","good":"诗意，善良的利他主义者，总是热情地为正当理由提供帮助。", "major": ["心理咨询师", "记者", "职业规划师", "建筑师", "律师", "编辑", "作家"]},
    "INTP": {"style": "逻辑学家人格","good":"具有创造力的发明家，对知识有着止不住的渴望。", "major": ["建筑师", "股票投资", "设计师", "音乐家", "医生", "律师"]},
    "ESTP": {"style": "企业家型人格","good":"聪明，精力充沛善于感知的人们。真心享受生活在边缘。", "major": ["消防员", "手工艺人", "企业家", "销售人员", "教练", "运动员", "记者", "游戏开发人员"]},
    "ESFP": {"style": "表演者型人格","good":"自发的，精力充沛而热情的表演者。生活在他们周围永不无聊。", "major": ["演员", "公关", "社会工作者", "教师", "销售人员", "兽医", "经纪人"]},
    "ENFP": {"style": "竞选者型人格","good":"热情，有创造力爱社交的自由自在的人，总能找到理由微笑。", "major": ["培训师", "人力资源管理人员", "社工", "心理学家", "记者", "咨询顾问", "编辑"]},
    "ENTP": {"style": "辩论家型人格","good":"聪明好奇的思想者，不会放弃任何智力上的挑战。", "major": ["企业家", "发明家", "主持人", "政客", "演员", "营销策划人员", "风险投资人"]},
    "ESTJ": {"style": "总经理型人格","good":"出色的管理者，在管理事情或人的方面无与伦比。", "major": ["营销人员", "行政管理", "管理人员", "律师", "公务员", "军官"]},
    "ESFJ": {"style": "执政官型人格","good":"极有同情心，爱交往受欢迎的人们，总是热心提供帮助极有同情心，爱交往受欢迎的人们，总是热心提供帮助。", "major": ["公关人员", "护士", "销售", "人力资源管理", "老师", "兽医"]},
    "ENFJ": {"style": "主人公型人格","good":"富有魅力鼓舞人心的领导者，有使听众着迷的能力。", "major": ["人力资源管理", "公益机构人员", "客户经理", "职业规划师", "培训师", "记者"]},
    "ENTJ": {"style": "指挥官型人格","good":"大胆，富有想象力且意志强大的领导者，总能我到或创造解决方法。", "major": ["公务员", "律师", "销售", "理财顾问", "经济分析师", "培训师", "程序员"]},
}

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
    st.markdown(f"## {personality_dict[personality_type]['style']}")
    st.markdown(f"{personality_dict[personality_type]['good']}")
    st.markdown(f"可能这种性格的职业:\n{personality_dict[personality_type]['major']}")
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


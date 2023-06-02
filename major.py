#!/usr/local/bin/python3

import openai
import json

openai.api_key_path = "/Users/liuchen/Desktop/lstreamlit/api-key"

get_info="""
{
  "gender":"男", //性别
  "subject":"理科",//文理科
  "MBTI":"ESFJ",//MBTI
  "evaluation":"很能理解他人的感受,从小都是班长" //自我评价
}
"""
# 定义模型
def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


# 根据信息输出文本建议
def text_output(input):
    major_prompt=f"""
        我是一个高三学生，刚参加完高考准备选专业，我的情况在会用json格式写出来: 
        {input} 

        整理以上信息,使用Markdown输出,示例()中为注意事项,输出不需要()中的内容:
        ```
        ## 1. 性格分析
        根据提供的信息，您的MBTI性格类型是xxxx。xxxx人群常常具备以下特点:
            - 优点：
                - xxxxxxxx(20字左右)
                - xxxxxxxx(20字左右)
            - 不足:
                - xxxxxxxx(20字左右)
                - xxxxxxxx(20字左右)

        ## 2. 专业选择建议
        基于您的个人情况，挑选了5个适合您的专业：

        xxxx：
            - 前景:xxxxxx (50字左右)
            - 依据:xxxxxx (注意结合自我介绍)
        ...

        ## 3. 相应职业机会
        以下是一些知名企业或事业单位招聘相应专业学生的职位：

        专业|知名企业或机构|职位
        ---|---|---
        xxx|xxx(2个以上)|xxx(2个以上)
        ```
        """
    output_text = get_completion(major_prompt, temperature=1)
    return output_text


def main(info):
    output_text = text_output(info)
    print(output_text)

    return output_text

if __name__ == "__main__" :
    main(get_info)

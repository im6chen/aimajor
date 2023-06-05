import os
# 文件路径
invitation_code_file = "./static/invitation_codes"

# 从文件中加载邀请码
def load_invitation_codes():
    if os.path.exists(invitation_code_file):
        with open(invitation_code_file, 'r') as file:
            return file.read().splitlines()
    else:
        return []

# 将新的邀请码保存到文件中
def save_invitation_code(code):
    with open(invitation_code_file, 'a') as file:
        file.write(code + '\n')

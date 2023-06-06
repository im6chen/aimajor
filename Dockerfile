# 基于Python镜像构建Docker镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制应用程序文件到容器中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器端口
EXPOSE 8501

# 运行应用程序
CMD ["streamlit", "run", "app.py"]


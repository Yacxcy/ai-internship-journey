# Stage 1: builder
# 使用Python 3.11 slim镜像作为构建阶段的基础镜像
FROM python:3.11-slim AS builder

# 设置工作目录为/app
WORKDIR /app

# 装uv
RUN pip install uv

# 复制依赖文件和源代码（editable install 需要源代码存在才能正确注册 app 包）
COPY pyproject.toml uv.lock* ./
COPY app ./app

# 安装依赖到虚拟环境（editable install，正确注册 app 包）
RUN uv venv && uv pip install -e .

# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（PDF 解析需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 复制虚拟环境
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# 复制应用代码
COPY app ./app
COPY data ./data

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
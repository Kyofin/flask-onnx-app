# Flask ONNX 模型推理 API

此项目提供了一个基于 Flask 的 API，用于使用 ONNX 模型进行推理。API 允许用户上传图像并根据模型的输出接收预测结果。用户可以替换模型并自定义类别标签。

## 特性

- **模型自定义**：轻松替换为你自己的 ONNX 模型。
- **标签自定义**：通过 API 请求定义你自己的类别标签。
- **图像推理**：上传图像进行分类并获取预测结果。

## 先决条件

- Python 3.8 或更高版本
- Docker（可选，用于容器化）

## 安装

1. **克隆仓库**：
    ```bash
    git clone https://github.com/yourusername/flask-onnx-inference.git
    cd flask-onnx-inference
    ```

2. **设置虚拟环境**：
    ```bash
    python -m venv venv
    source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
    ```

3. **安装依赖**：
    ```bash
    pip install flask onnxruntime Pillow
    ```

## 使用

### 本地运行

1. **启动 Flask 应用**：
    ```bash
    python app.py
    ```

2. **发送 POST 请求到 `/predict` 端点**：
    - 使用 Postman 或 `curl` 等工具发送带有图像文件和类别标签的 POST 请求。

    使用 `curl` 的示例：
    ```bash
    curl -X POST -F "file=@/path/to/your/image.jpg" -F "labels=['Apple', 'Banana']" http://localhost:5000/predict
    ```

### 使用 Docker 运行

#### 从阿里云镜像仓库下载并运行

1. **拉取 Docker 镜像**：
    ```bash
    docker pull registry.cn-hangzhou.aliyuncs.com/cum/flask-onnx-app:latest
    ```

2. **运行 Docker 容器并挂载模型文件**：
    ```bash
    docker run -d -p 5000:5000 -v /path/to/your/model.onnx:/app/model.onnx registry.cn-hangzhou.aliyuncs.com/cum/flask-onnx-app:latest
    ```

    请将 `/path/to/your/model.onnx` 替换为你本地模型文件的实际路径。

3. **发送 POST 请求到 `/predict` 端点**：
    - 使用 Postman 或 `curl` 等工具发送带有图像文件和类别标签的 POST 请求。

    使用 `curl` 的示例：
    ```bash
    curl -X POST -F "file=@/path/to/your/image.jpg" -F "labels=['Apple', 'Banana']" http://localhost:5000/predict
    ```

#### 构建并推送镜像到阿里云镜像仓库

1. **登录阿里云镜像仓库**：
    ```bash
    docker login --username=your_username registry.cn-hangzhou.aliyuncs.com
    ```

2. **构建 Docker 镜像**：
    ```bash
    docker build -t flask-onnx-app .
    ```

3. **标记 Docker 镜像**：
    ```bash
    docker tag flask-onnx-app registry.cn-hangzhou.aliyuncs.com/cum/flask-onnx-app:latest
    ```

4. **推送 Docker 镜像**：
    ```bash
    docker push registry.cn-hangzhou.aliyuncs.com/cum/flask-onnx-app:latest
    ```

### 自定义模型和标签

- **替换模型**：
    - 将你的 ONNX 模型文件放置在 `/app` 目录中，并在 `app.py` 中更新 `model_path` 变量。

- **自定义标签**：
    - 在 POST 请求的 `labels` 字段中传递类别标签的 JSON 数组。

## 示例响应

```json
{
    "predicted_class": "Apple",
    "probability": 0.987654321
}

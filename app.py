from flask import Flask, request, jsonify
import onnxruntime as ort
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# 加载ONNX模型
model_path = '/app/model.onnx'
ort_session = ort.InferenceSession(model_path)

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((640, 640))  # 根据模型输入尺寸调整图片大小
    image = np.array(image).astype(np.float32)  # 转换为numpy数组并转换数据类型
    image = image / 255.0  # 归一化
    image = np.transpose(image, (2, 0, 1))  # 调整通道顺序
    image = np.expand_dims(image, axis=0)  # 增加批次维度
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 获取类别标签
    class_labels = request.form.get('labels')
    if not class_labels:
        return jsonify({'error': 'No labels provided'}), 400

    try:
        class_labels = eval(class_labels)  # 将字符串转换为列表
        if not isinstance(class_labels, list) or not all(isinstance(label, str) for label in class_labels):
            return jsonify({'error': 'Invalid labels format'}), 400

        image_bytes = file.read()
        image = preprocess_image(image_bytes)

        # 进行推理
        input_name = ort_session.get_inputs()[0].name
        output_name = ort_session.get_outputs()[0].name
        predictions = ort_session.run([output_name], {input_name: image})[0]

        # 解析结果
        class_index = np.argmax(predictions)
        class_prob = predictions[0, class_index]
        predicted_class = class_labels[class_index]

        return jsonify({
            'predicted_class': predicted_class,
            'probability': float(class_prob)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

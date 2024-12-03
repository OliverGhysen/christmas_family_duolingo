from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/get_images/<grandchild>', methods=['GET'])
def get_images(grandchild):
    folder_path = f'static/pics_{grandchild}'
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder not found'}), 404
    
    images = [file for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True)

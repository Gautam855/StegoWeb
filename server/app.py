from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from stegano import lsb
from PIL import Image, ImageTk
import base64
from vigenre import encrypt_vigenere, decrypt_vigenere
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/encrypt_text', methods=['POST'])
def encrypt_text():
    try:
        # Retrieve image, text data, and password from the request
        image_file = request.files['image']
        text = request.form['text']
        password = request.form['password']
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        print(f"Image file saved: {filepath}")
        print(f"Text to encrypt: {text}")
        print(f"Password: {password}")

        # Add a known marker to the text
        marker = "VALID:"
        marked_text = marker + text

        # Perform encryption
        encrypted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"encrypted_{filename}")
        cipher_text = encrypt_vigenere(marked_text, password)
        secret = lsb.hide(filepath, cipher_text, None, 69, "UTF-8")
        secret.save(encrypted_image_path)
        print(f"Encrypted image saved: {encrypted_image_path}")
    except KeyError as e:
        return jsonify({"error": str(e)}), 400

    return send_file(encrypted_image_path, as_attachment=True)

@app.route('/decrypt_text', methods=['POST'])
def decrypt_text():
    try:
        # Retrieve image and password from the request
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['image']
        password = request.form['password']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            decrypted_message = lsb.reveal(filepath, None, 69, "UTF-8")
            if decrypted_message is None:
                return jsonify({"error": "No hidden message found"}), 400

            # Decrypt the message using the provided password
            plain_text = decrypt_vigenere(decrypted_message, password)

            # Check if the message contains the marker
            marker = "VALID:"
            if plain_text.startswith(marker):
                actual_message = plain_text[len(marker):]
                return jsonify({"text": actual_message})
            else:
                return jsonify({"error": "Incorrect password"}), 400
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/decrypt_Image', methods=['POST'])
def decrypt_Image():
    try:
        # Retrieve image and password from the request
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['image']
        password = request.form['password']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Reveal the hidden message
            decrypted_image_str = lsb.reveal(filepath)
            if decrypted_image_str is None:
                os.remove(filepath)  # Clean up the saved file
                return jsonify({"error": "No hidden message found"}), 400

            # Decrypt the base64-encoded image string
            # decrypted_image_str = decrypt_vigenere(decrypted_image_base64, password)

            # Check if the message contains the marker
            marker = "VALID:"
            if decrypted_image_str.startswith(marker):
                decrypted_image_base64 = decrypted_image_str[len(marker):]
                print(decrypted_image_base64)
                decrypted_image_bytes = base64.b64decode(decrypted_image_base64)
                decrypted_image_file = BytesIO(decrypted_image_bytes)
                oimg = Image.open(decrypted_image_file)

            # Convert to RGB mode
                out_jpg = oimg.convert('RGB')

                secret_image10_path = os.path.join(app.config['UPLOAD_FOLDER'], 'secret_image10.png')
                out_jpg.save(secret_image10_path)  # Clean up the saved file
                return send_file(secret_image10_path, as_attachment=True)
                # Return the decrypted image as a response
                # return send_file(out_jpg, as_attachment=True, download_name='decrypted_image.png', mimetype='image/png')
            else:
                print("pass wrong")
                os.remove(filepath)  # Clean up the saved file
                return jsonify({"error": "Incorrect password"}), 400
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/encrypt_images', methods=['POST'])
def encrypt_images():
    try:
        # Check if the post request has the file parts and password
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({"error": "No file part"}), 400
        image1 = request.files['image1']
        image2 = request.files['image2']
        password = request.form['password']

        # If user does not select file, browser also
        # submit an empty part without filename
        if image1.filename == '' or image2.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if image1 and allowed_file(image1.filename) and image2 and allowed_file(image2.filename):
            # Save the images to the upload folder
            filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image1.filename))
            filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image2.filename))
            image1.save(filepath1)
            image2.save(filepath2)

            # Convert the second image to a base64 string
            with open(filepath2, 'rb') as img_file:
                image2_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # Encrypt the base64 string using the provided password
            marker = "VALID:"
            print(image2_base64)
            encrypted_image2_base64 = marker + image2_base64
            print("normal \n\n\n\n\n",encrypted_image2_base64)
            # encrypted_image2_base64 = encrypt_vigenere(marked_image2_base64, password)
            # print("encrypted \n\n\n\n\n",encrypted_image2_base64)
            # Hide the encrypted image string within the first image using LSB steganography
            secret_image = lsb.hide(filepath1, encrypted_image2_base64)
            # temp=secret_image
            # image2_base649 = base64.b64encode(temp.read()).decode('utf-8')

            # image2_base64 = base64.b64encode(i_file.read()).decode('utf-8')

            # print("secret \n\n\n\n\n\n",temp)
            # Save the resulting image
            secret_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_image.png')
            secret_image.save(secret_image_path)

            # Return the resulting image as an attachment
            print("success")
            # image2_base649 = base64.b64encode(secret_image.read()).decode('utf-8')
            return send_file(secret_image_path, as_attachment=True)
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

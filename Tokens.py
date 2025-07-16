from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

PORT = int(os.getenv("PORT", 5000))

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Token Fetcher</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #FF69B4;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 80%;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background-color: #FF1493;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                text-align: center;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            input[type="text"], input[type="password"] {
                padding: 10px;
                margin: 10px 0;
                width: 80%;
                max-width: 400px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            footer {
                margin-top: 30px;
                padding: 10px;
                background-color: #333;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                text-align: center;
            }
            footer a {
                color: #4CAF50;
                text-decoration: none;
                font-weight: bold;
            }
            footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Login to Facebook and Get Token</h2>
            <form action="/get_token" method="POST">
                <label for="username">Username (Email):</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Get Token">
            </form>
        </div>
        <footer>
            Developed by <a href="#">rahul</a>
        </footer>
    </body>
    </html>
    """)

@app.route('/get_token', methods=['POST'])
def get_token():
    user = request.form['username']
    passw = request.form['password']

    login_url = (
        'https://b-api.facebook.com/method/auth.login'
        '?access_token=237759909591655%257C0f140aabedfb65ac27a739ed1a2263b1'
        '&format=json'
        '&sdk_version=2'
        f'&email={user}'
        f'&locale=en_US'
        f'&password={passw}'
        '&sdk=ios'
        '&generate_session_cookies=1'
        '&sig=3f555f99fb61fcd7aa0c44f58f522ef6'
    )

    response = requests.get(login_url)
    data = response.json()

    if "session_key" in data:
        token = data.get("access_token")
        user_info_url = f"https://graph.facebook.com/me?access_token={token}"
        user_info_response = requests.get(user_info_url)
        user_info = user_info_response.json()

        name = user_info.get("name", "Failed to retrieve account name.")
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Token Retrieved</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    max-width: 900px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }
                h2 {
                    text-align: center;
                    color: #333;
                }
                .result-box {
                    margin-top: 30px;
                    padding: 20px;
                    border: 2px solid #ddd;
                    background-color: #f9f9f9;
                    border-radius: 6px;
                }
                .token-box {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #e3f2fd;
                    border: 1px solid #2196F3;
                    border-radius: 5px;
                    word-wrap: break-word;
                }
                footer {
                    margin-top: 30px;
                    padding: 10px;
                    background-color: #333;
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                    text-align: center;
                }
                footer a {
                    color: #4CAF50;
                    text-decoration: none;
                    font-weight: bold;
                }
                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Token Retrieved Successfully!</h2>
                <div class="result-box">
                    <p><strong>Username:</strong> {{ username }}</p>
                    <p><strong>Account Name:</strong> {{ name }}</p>
                    <div class="token-box">
                        <p><strong>Token:</strong></p>
                        <p>{{ token }}</p>
                    </div>
                </div>
            </div>
            <footer>
                Developed by <a href="#">Rahul</a>
            </footer>
        </body>
        </html>
        """, username=user, token=token, name=name)

    else:
        return "Invalid username/password. Please try again."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)

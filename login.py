import panel as pn 
from panel.custom import Child, ReactiveHTML

pn.extenstion()

class LoginLayout(ReactiveHTML):
    
    _template = """


            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CDAO CARD Application | Login</title>
               <!-- <link rel="icon" type="image/x-icon" href="{{ PANEL_CDN }}images/favicon.ico"> -->
                <style>
                    * {
                        box-sizing: border-box;
                        margin: 0;
                        padding: 0;
                    }
                    html, body {
                        height: 100%;
                        font-family: 'Segoe UI', sans-serif;
                        background-color: #f5f5f5;
                        color: #333;
                    }
                    .container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                    }
                    .login-form {
                        background-color: #fff;
                        padding: 2rem;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        width: 100%;
                        max-width: 400px;
                    }
                    .form-header {
                        text-align: center;
                        margin-bottom: 2rem;
                    }
                    #logo {
                        margin-bottom: 1rem;
                    }
                    .form-header h3 {
                        margin-bottom: 0.5rem;
                        font-size: 1.5rem;
                    }
                    .form-header p {
                        font-size: 1rem;
                        color: #777;
                    }
                    .form-group {
                        margin-bottom: 1.5rem;
                    }
                    .form-input {
                        width: 100%;
                        padding: 0.75rem;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        font-size: 1rem;
                        background-color: #fafafa;
                    }
                    .form-input:focus {
                        outline: none;
                        border-color: #107bba;
                    }
                    .form-button {
                        width: 100%;
                        padding: 0.75rem;
                        background-color: #107bba;
                        border: none;
                        border-radius: 4px;
                        color: #fff;
                        font-size: 1rem;
                        text-transform: uppercase;
                        cursor: pointer;
                    }
                    .form-button:hover {
                        background-color: #0a6691;
                    }
                    .error-message {
                        color: #e74c3c;
                        font-weight: bold;
                        text-align: center;
                        margin-bottom: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <form class="login-form" action=${action} method="post">
                        <div class="form-header">
                           <!-- <img id="logo" src="{{ PANEL_CDN }}images/logo_stacked.png" width="150" height="120" alt="CDAO Logo"> -->
                            <h3>CDAO CARD Application</h3>
                            <p>Login to access the Cost Analysis Requirements Document system</p>
                        </div>
                        <!-- <div id="error-message" class="error-message">{{errormessage}}</div> -->
                        <div class="form-group">
                            <input name="username" type="text" class="form-input" autocapitalize="off" autocorrect="off" placeholder="Username" required>
                        </div>
                        <div class="form-group">
                            <input name="password" type="password" class="form-input" placeholder="Password" required>
                        </div>
                        <div class="form-group">
                            <button class="form-button" type="submit">Login</button>
                        </div>
                    </form>
                </div>
            </body>
            </html>
            """
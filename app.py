from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Здесь вы можете задать свои собственные имя пользователя и пароль
USERNAME = os.getenv("ADMIN_USERNAME", "admin")
PASSWORD = os.getenv("ADMIN_PASSWORD", "password")

# Получаем пароль VNC из переменных окружения
VNC_PASSWORD = os.getenv("VNC_PASSWORD", "vncpassword")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Arial, sans-serif;
            }
            .login-container {
                width: 300px;
                margin: 100px auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .login-container input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
            .login-container button {
                width: 100%;
                padding: 10px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            }
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=login_html)


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/", status_code=303)
    else:
        error_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Error</title>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    font-family: Arial, sans-serif;
                }
                .error-container {
                    width: 300px;
                    margin: 100px auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    text-align: center;
                }
                .error {
                    color: red;
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                <h2 class="error">Invalid credentials</h2>
                <a href="/login">Try again</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")

    index_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Browser Agent</title>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
                background: #000;
            }}
            .container {{
                display: flex;
                height: calc(100vh - 40px);
                position: relative;
            }}
            .frame {{
                height: 100%;
                width: 100%;
                border: none;
            }}
            .frame-container {{
                height: 100%;
            }}
            #left-container {{
                width: 50%;
            }}
            #right-container {{
                width: 50%;
            }}
            .logout-btn {{
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 5px 10px;
                background-color: #dc3545;
                color: white;
                text-decoration: none;
                border-radius: 3px;
                z-index: 20;
            }}
        </style>
    </head>
    <body>
        <div class="container" id="container">
            <div class="frame-container" id="left-container">
                <iframe class="frame" id="left-frame" src="http://0.0.0.0:7788/" allowfullscreen></iframe>
            </div>
            <div class="frame-container" id="right-container">
                <iframe class="frame" id="right-frame" src="http://0.0.0.0:6080/vnc.html?password={VNC_PASSWORD}" allowfullscreen></iframe>
            </div>
        </div>
        <a href="/logout" class="logout-btn">Logout</a>
    </body>
    </html>
    """
    return HTMLResponse(content=index_html)


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("authenticated", None)
    return RedirectResponse(url="/login")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9220)
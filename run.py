import os
from form import app,db

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port="5000",
        debug="DEBUG",
    )
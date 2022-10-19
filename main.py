from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_index_html():
    with open("index.html", "r") as fh:
        data = fh.read()

    return Response(content=data, media_type="text/html")

@app.get("/sql/{student_name}")
def get_student_info(student_name: str):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("select * from tbStudent where name = \"%s\"" % (student_name,))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.executescript('''
        DROP TABLE IF EXISTS tbStudent;
        CREATE TABLE tbStudent(
            name varchar(255) primary key,
            class varchar(10) not null,
            grade float not null
        );

        INSERT INTO tbStudent VALUES("Tan", "IA1501", 9.9);
        INSERT INTO tbStudent VALUES("Phi Truong", "IA1501", 10.1);
        INSERT INTO tbStudent VALUES("Hai", "IA1501", 10);
    ''')

    uvicorn.run(app, host='127.0.0.1', port=8080)
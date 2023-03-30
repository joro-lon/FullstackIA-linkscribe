from fastapi import FastAPI, Response, status, HTTPException, Depends
import models as models
from schemas import users
from schemas import links
from schemas import msglink
from ORM import engine, get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import nltk
nltk.download("punkt")
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import *
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def getAll(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = [title.get_text() for title in soup.find_all('title')]
    title = "".join(title)
    content = [parr.get_text() for parr in soup.find_all("p")]
    text_join = " ".join(content)
    parse = PlaintextParser.from_string(text_join, Tokenizer("english"))
    summarizer_Lex = LexRankSummarizer()
    summary_Lex = summarizer_Lex(parse.document, 5)
    lex_summary=""
    for sentence in summary_Lex:
        lex_summary+=str(sentence)

    options = webdriver.ChromeOptions() 
    options.add_argument('--window-size=1000,500') 
    options.add_argument('--headless') #para que chrome se ejecute sin necesidad de iniciar la interfaz gráfica
    #options.add_argument('--disable-gpu') #parámetro necesario si usamos Windows como sistema operativo.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options, executable_path="chromedriver")
    #driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.get(url)
    driver.save_screenshot('screen.png')
    driver.quit()

    return {'link': url, 'title': title, 'summary': lex_summary}
        
def getImage():
    im = Image.open("screen.png")
    im = im.convert("RGB")
    im_io = BytesIO()
    # create in-memory JPEG in RAM (not disk)
    im.save(im_io, 'JPEG', quality=50)

    # get the JPEG image in a variable called JPEG
    JPEG = im_io.get_value()

    return Response(content = JPEG, media_type="image/jpeg")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/search",
    "http://localhost:3000/searchaccount"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post:users, db: Session = Depends(get_db)):
    print(post)
    new_post = models.users(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post.dict()

@app.post("/links/", status_code = status.HTTP_201_CREATED)
def create_links(post:links, db: Session = Depends(get_db)):
    print(post)
    new_post = models.links(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post.dict()

@app.get("/posts/{name}-{password}", response_model=users)
def get_post(name: str, password: str, db: Session = Depends(get_db)):
    post = db.query(models.users).filter(models.users.name == name).first()
    if post == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with name: {name} was not found")
    if post.password == password:
        return post
    else:
        return {}
    
@app.get("/links/{id}")
def get_links(id: int, db: Session = Depends(get_db)):
    post = db.query(models.links).filter(models.links.user_id == id).all()
    if post == []:
        return [{}]
    return post

@app.post("/nlp/")
def get_contain(link: msglink):
    dict_response = getAll(link.link)
    return dict_response

@app.get("/nlpimage/")
def get_contain2():
    im = Image.open("screen.png")
    im = im.convert("RGB")
    im_io = BytesIO()
    # create in-memory JPEG in RAM (not disk)
    im.save(im_io, 'JPEG', quality=100)

    # get the JPEG image in a variable called JPEG
    JPEG = im_io.getvalue()

    return Response(content = JPEG, media_type="image/jpeg")



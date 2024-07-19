from database import SessionLocal
from models import Question
from datetime import datetime
import random

rand_content = ['내용무','섹스','성발기충','보지털황제','나다 병신아.']
db = SessionLocal()
for i in range(300):
    q = Question(subject='테스트 데이터입니다:[%03d]' % i, content=random.choice(rand_content), create_date=datetime.now())
    db.add(q)
db.commit()
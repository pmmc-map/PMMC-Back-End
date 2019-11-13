import csv
import pandas as pd
from app import app, db
from app.models import Location, CityImages
from app.survey import Question, Response, Option
from flask_cors import CORS, cross_origin



def sql_to_csv(tables=[Question, Response, Option], key='qid', name='mydump'):
    combined = db.session.query(*tables)
    for table in tables[1:]:
        combined = combined.join(table)#, tables[0].qid == table.qid) USE IF NOT USING FOREIGN KEYS

    df = pd.read_sql(combined.statement, db.session.bind)
    df = df.loc[:,~df.columns.duplicated()]
    del df[key] 
    df.to_csv(name, index=False) 
    return open(name + '.csv', 'w'), name 


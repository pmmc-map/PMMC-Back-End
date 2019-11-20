import csv
import pandas as pd
from app import app, db
from app.models import Location, CityImages
from app.survey import Question, VisitorResponse, Option
from flask_cors import CORS, cross_origin

def sql_to_csv(tables=[Question, VisitorResponse, Option], key='qid', name='mydump'):
    tables = [Question, Option]
    combined = db.session.query(Question)
    #print(combined)
    #exit()
    combined = combined.join(Option)
    print("------Combined 1-------")
    print(combined)
    print("------Combined 2-------")
    combined = combined.join(VisitorResponse)
    print(combined)
    # for table in tables[1:]:
    #     combined = combined.join(table)#, tables[0].qid == table.qid) USE IF NOT USING FOREIGN KEYS
    
    df = pd.read_sql(combined.statement, db.session.bind)
    df = df.loc[:,~df.columns.duplicated()]
    del df[key] 
    df.to_csv(name, index=False)
    print(df)
    return open(name + '.csv', 'w'), name

if __name__=="__main__":
    sql_to_csv()

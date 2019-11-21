import csv
import pandas as pd
from app import app, db
from app.models import Location, CityImages
from app.survey import Question, Option, VisitorResponse
from flask_cors import CORS, cross_origin



def sql_to_csv(tables=[Question, Option, VisitorResponse], name='mydump'):
    if len(tables) == 1:
    	df = pd.read_sql(db.session.query(tables[0]).statement, db.session.bind)
    	df.to_csv(name + '.csv', index=False) 
    else:
    	combined = db.session.query(tables[0])
    	combined = combined.join(tables[1])
    	combined = combined.join(tables[2], tables[1].oid == tables[2].oid)
    	df = pd.read_sql(combined.statement, db.session.bind)
    	print(df)
    	# df = df.loc[:,~df.columns.duplicated()]
    	df.to_csv(name+ '.csv', index=False) 
    return open(name + '.csv', 'w')
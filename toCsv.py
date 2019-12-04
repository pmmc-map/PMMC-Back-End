import csv
from app import app, db
from app.models import Location, CityImages, DonationVisit
from app.survey import Question, Option, VisitorResponse

def survey_to_csv():
	submitted = VisitorResponse.query.join(Option).add_columns(VisitorResponse.vr_timestamp, Option.text.label("option_text")).filter_by(oid=Option.oid).join(Question).add_columns(Question.text.label("question_text")).filter_by(qid=Question.qid).all()

	with open('survey.csv', 'w') as f:
		out = csv.writer(f)
		out.writerow(['question', 'option_selected', 'timestamp'])

		for item in submitted:
			out.writerow([item.question_text, item.option_text, item.vr_timestamp])
	return open('survey.csv', 'rb')

def pin_to_csv():
	submitted = Location.query.all()

	with open('pin_info.csv', 'w') as f:
		out = csv.writer(f)
		out.writerow(['city', 'state', 'country', 'visit_date'])

		for item in submitted:
			out.writerow([item.city, item.state, item.country, item.visit_date])
	return open('pin_info.csv', 'rb')

def donation_to_csv():
	submitted = DonationVisit.query.all()

	with open('donation_visits.csv', 'w') as f:
		out = csv.writer(f)
		out.writerow(['visit_counter', 'timestamp'])

		for item in submitted:
			out.writerow([item.dvid, item.dv_timestamp])
	return open('donation_visits.csv', 'rb')

# if __name__=="__main__":
# 	survey_to_csv()
# 	pin_to_csv()
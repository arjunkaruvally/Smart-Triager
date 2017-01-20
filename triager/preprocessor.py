from utility.MLStripper import MLStripper
from utility.CouchInterface import CouchInterface 
from mappings.Ticket import Ticket
import datetime

class Tickets:

	def strip_tags(self, html): #helper function to sanitize html tags in comments
	    s = MLStripper()
	    s.feed(html)
	    return s.get_data()

	def upload_tickets(self, file_path="data/Ticket_list.xlsx", worksheet="Tickets in Queue with History", upload=True):
		from openpyxl import load_workbook
		
		wb = load_workbook(file_path, read_only=True)
		ws = wb[worksheet]
		rowi = 0
		coli = 0
		template = {}
		template_keys = []
		document = []
		document_ord = []

		for row in ws.rows:
			rowi = rowi+1
			coli = 0

			if rowi < 2:
				for col in row:
					template[col.value] = ''
					template_keys.append(col.value)
			else:
				for col in row:
					if coli==0 and (col.value==None or col.value==''):
						break
					if col.value==None:
						val = ''
					else:
						val = col.value
					template[template_keys[coli]] = val
					coli=coli+1

				template['Comments'] = self.strip_tags(template['Comments'])
				template['Alert Comments'] = self.strip_tags(template['Alert Comments'])
				template['Comments'] = template['Comments'].replace('_x000D_',' ')
				template['Alert Comments'] = template['Alert Comments'].replace('_x000D_',' ')
				template['Comments'] = template['Comments'].replace('\n',' ')
				template['Alert Comments'] = template['Alert Comments'].replace('\n',' ')

				temp = Ticket(
						ticket_number = template[template_keys[0]],
						account_name = template[template_keys[1]],
						severity = template[template_keys[2]],
						service_offering = template[template_keys[3]],
						action = template[template_keys[4]],
						action_past_tense = template[template_keys[5]],
						action_date = template[template_keys[6]],
						status = template[template_keys[7]],
						assigned_to_csr = template[template_keys[8]],
						performed_by_csr = template[template_keys[9]],
						new_queue = template[template_keys[10]],
						category = template[template_keys[11]],
						comments = template[template_keys[12]],
						summary = template[template_keys[13]],
						additional_info_1 = template[template_keys[14]],
						additional_info_2 = template[template_keys[15]],
						alert_indicator = template[template_keys[16]],
						alert_comments = template[template_keys[17]],
						detail = template[template_keys[18]]
					)

				document.append(temp)
				document_ord.append(template)
		# print len(document)
		# print document[0]
		# print "\n"
		# print document[0]['Ticket Number']
		# print self.strip_tags(document[0]['Comments'])
		
		if upload:
			dbinter = CouchInterface()

			print "Uploading "+str(len(document))+" tickets to database"
			n_success = dbinter.add_documents('triager_tickets', document)
			n_failed = len(document)-n_success
			print "Upload Complete"
			print str(len(document))+" documents processed"
			print str(n_success)+" document successfully uploaded"
			print str(n_failed)+" documents failed!!"

		return document_ord
	###Use these functions only if data is available in the database
	# def predict_category() #Predict the category field of unknown category tickets
		

tkt = Tickets()
tkt.upload_tickets()
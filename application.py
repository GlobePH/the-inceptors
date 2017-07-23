from flask import Flask, request, jsonify, render_template
import sqlite3
import requests
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")
	
@app.route('/esprequestproducer', methods=['GET', 'POST'])
def esprequestproducer():
		if request.method == 'GET':
		    return 'Please use POST request only'
		elif request.method == 'POST':
			"""
			 {
			  "espid": 1,
		      "consumption": {
		          "voltage": 1,
		          "current": 1
		      },
		      "distribution": {
		          "voltage": 1,
		          "current": 1
		      },
			  "switch": false,
		      "timestamp": "timestamp"
		    }
			"""
			
			esp_data = request.get_json()
			
			eps_id = esp_data["espid"]
			consumption = esp_data["consumption"]
			distribution = esp_data["distribution"]
			switch = esp_data["switch"]
			
			insert_stmt = """INSERT INTO producer_table 
								(esp_id,
								voltage_consumption,
								current_consumption,
								voltage_distribution,
								current_distribution,
								switch) 
							VALUES (?, ?, ?, ?, ?, ?)"""
			values = (eps_id, 
						consumption["voltage"],
						consumption["current"],
						distribution["voltage"],
						distribution["current"],
						switch,
			)
								
			with sqlite3.connect('inteliqas.db') as conn:
				c = conn.cursor()
				c.execute("""SELECT count(*) FROM producer_table""")
				count_rows = c.fetchall()
				count_row = count_rows[0]
				if int(count_row[0]) == 0:
					c.execute(insert_stmt, values)
					return "INITIAL INSERT"			
				else:
					c.execute("""SELECT (julianday(CURRENT_TIMESTAMP) - julianday(timestamp)) * 1440 
									FROM producer_table 
									ORDER BY timestamp 
									DESC LIMIT 1""")			
					time_rows = c.fetchall()
					time_row = time_rows[0]
					if round(float(time_row[0])) > .1:
						c.execute(insert_stmt, values)
					c.execute("""SELECT esp_id,
									switch
									FROM producer_table 
									ORDER BY timestamp 
									DESC LIMIT 1""")			
					rows = c.fetchall()
					row = rows[0]
					json_response = {
						"espid": row[0],
						"switch": row[1]
					}
					return jsonify(json_response)
			
@app.route('/esprequestconsumer', methods=['GET', 'POST'])
def esprequestconsumer():
		if request.method == 'GET':
		    return 'Please use POST request only'
		elif request.method == 'POST':
			"""
			 {
			  "espid": 1,
		      "consumption": {
		          "voltage": 1,
		          "current": 1
		      },
		      "distribution": {
		          "voltage": 1,
		          "current": 1
		      },
		      "branch1": false,
		      "branch2": false,
		      "branch3": false,
		      "branch4": true,
		      "timestamp": "timestamp"
		    }
			"""
			
			esp_data = request.get_json()
			
			eps_id = esp_data["espid"]
			consumption = esp_data["consumption"]
			branch1 = esp_data["branch1"]
			branch2 = esp_data["branch2"]
			branch3 = esp_data["branch3"]
			branch4 = esp_data["branch4"]
			
			insert_stmt = """INSERT INTO producer_table 
								(esp_id,
								voltage_consumption,
								current_consumption,
								branch1,
								branch2,
								branch3,
								branch4) 
							VALUES (?, ?, ?, ?, ?, ?, ?)"""
			values = (eps_id, 
						consumption["voltage"],
						consumption["current"],
						branch1,
						branch2,
						branch3,
						branch4,
			)
								
			with sqlite3.connect('inteliqas.db') as conn:
				c = conn.cursor()
				c.execute("""SELECT count(*) FROM producer_table""")
				count_rows = c.fetchall()
				count_row = count_rows[0]
				if int(count_row[0]) == 0:
					c.execute(insert_stmt, values)
					return "INITIAL INSERT"			
				else:
					c.execute("""SELECT (julianday(CURRENT_TIMESTAMP) - julianday(timestamp)) * 1440 
									FROM producer_table 
									ORDER BY timestamp 
									DESC LIMIT 1""")			
					time_rows = c.fetchall()
					time_row = time_rows[0]
					if round(float(time_row[0])) > 1:
						c.execute(insert_stmt, values)
					c.execute("""SELECT esp_id,
									branch1,
									branch2,
									branch3,
									branch4
									FROM producer_table 
									ORDER BY timestamp 
									DESC LIMIT 1""")			
					rows = c.fetchall()
					row = rows[0]
					json_response = {
						"espid": row[0],
						"branch1": row[1],
						"branch2": row[2],
						"branch3": row[3],
						"branch4": row[4],
					}
					return jsonify(json_response)
					
@app.route('/rnrequest', methods=['GET', 'POST'])
def rnrequest():
		if request.method == 'GET':
		    return 'Please use POST request only'
		elif request.method == 'POST':
			"""
			 {
			  "mode": "update",
			  "type": "consumer",
			  "username": "inteliqas",
			  "mobile_id": 1,
			  "payment_done": false,
			  "payment_timestamp": "2017-07-22 13:14:36",
			  "payment_amount": 1,
			  "kwhr_bought":1,
		      "branch1": false,
		      "branch2": false,
		      "branch3": false,
		      "branch4": true,
		      "timestamp": "timestamp"
		    }
			"""
			# mobile_data = json.loads(request.data.decode('UTF-8').split()[0])
			if not request.form.get("username"):
				return "must provide old username"
			else:
				username = request.form.get("username")
			# mode = mobile_data["mode"]
			# username = mobile_data["username"]
			# mobile_id = mobile_data["mobile_id"]
			# payment_done = mobile_data["payment_done"]
			# payment_timestamp = mobile_data["payment_timestamp"]
			# payment_amount = mobile_data["payment_amount"]
			# kwhr_bought = mobile_data["kwhr_bought"]
			# branch1 = mobile_data["branch1"]
			# branch2 = mobile_data["branch2"]
			# branch3 = mobile_data["branch3"]
			# branch4 = mobile_data["branch4"]
			
			with sqlite3.connect('inteliqas.db') as conn:
				c = conn.cursor()
				
				# if mode == "update":				
					# c.execute("""UPDATE consumer_table 
					# 			SET mobile_id = ?,
					# 			payment_done = ?,
					# 			payment_timestamp = ?,
					# 			payment_amount = ?,
					# 			kwhr_bought = ?,
					# 			branch1 = ?,
					# 			branch2 = ?,
					# 			branch3 = ?,
					# 			branch4 = ?
					# 			WHERE timestamp = (SELECT timestamp
					# 			FROM producer_table 
					# 			ORDER BY timestamp 
					# 			DESC LIMIT 1)
					# 			""",
					# 			(mobile_id,
					# 			payment_done,
					# 			payment_timestamp,
					# 			payment_amount,
					# 			kwhr_bought,
					# 			branch1,
					# 			branch2,
					# 			branch3,
					# 			branch4
					# 			))
				c.execute("""SELECT *
							FROM producer_table 
							ORDER BY timestamp 
							DESC LIMIT 1""")
				rows_producer = c.fetchall()
				row_producer = rows_producer[0]
				# json_response = {
					# "espid": row[1],
					# "mobile_id": row[2],
				voltage_consumption = row_producer[3]
				current_consumption = row_producer[4]
				voltage_distribution = row_producer[5]
				current_distribution = row_producer[6]
				
				c.execute("""SELECT *
							FROM consumer_table 
							ORDER BY timestamp 
							DESC LIMIT 1""")
				rows_consumer = c.fetchall()
				row_consumer = rows_consumer[0]
				# json_response = {
					# "espid": row[1],
					# "mobile_id": row[2],
				voltage_consumption_c = row_consumer[7]
				current_consumption_c = row_consumer[8]
					# "username": row[9]
				# }
				# print(jsonify(json_response))
				# return jsonify(json_response)
				power_distribution = voltage_distribution*voltage_distribution
				power_consumption = voltage_consumption*voltage_consumption
				power_consumption_c = voltage_consumption_c*current_consumption_c
				return render_template('dashboard.html', voltage_distribution=voltage_distribution, current_distribution=current_distribution,
				voltage_consumption=voltage_consumption, current_consumption=current_consumption,
				voltage_consumption_c=voltage_consumption_c, current_consumption_c=current_consumption_c,
				power_distribution=power_distribution,
				power_consumption=power_consumption,
				power_consumption_c=power_consumption_c)
				
@app.route('/payment', methods=['GET', 'POST'])
def payment1():
		if request.method == 'GET':
		    return 'Please use POST request only'
		elif request.method == 'POST':
			"""
			 {
			  "mode": "payment",
			  "type": "consumer",
			  "mobile_id": 1,
			  "payment_done": false,
			  "payment_timestamp": "2017-07-22 13:14:36",
			  "payment_amount": 1,
			  "kwhr_bought":1,
		      "timestamp": "timestamp"
		    }
			"""
			
			payment_data = request.get_json()
			
			mobile_id = payment_data["mobile_id"]
			
			with sqlite3.connect('inteliqas.db') as conn:
				c = conn.cursor()
				c.execute("""SELECT consumer_id
							FROM consumer_table
							WHERE mobile_id = ?
							LIMIT 1""")
				rows = c.fetchall()
				row = rows[0]
				json_response = {
					"consumer_id": row[1]
				}
			return jsonify(json_response)
				
if __name__ == '__main__':
  app.run(debug=True)
import csv
import os

def read_data():
	try:
		return sum([int(c) for c in input()])
	except: return None

num_data = read_data()
data_names = []

for i in range(num_data):
	name = ""
	char = read_data()
	while char != 62:
		name += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[char]
		char = read_data()
	data_names.append(name)

with open('microbit_data.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(data_names)
	try:
		while True:
			d = []
			for i in range(num_data):
				d.append(read_data())
				if None in d:
					break;
			if None in d or len(d) != num_data:
				break;
			writer.writerow(d)
	except Exception as e: print("\nFailed collecting data:", e)

print("\nOpening file...")
os.system("python3 microbit_data_viewer.py")

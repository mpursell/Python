import os

def main():

	myPath = raw_input("Enter a path:  ")
	myFile = raw_input("Enter a filename:  ")
	csvFile = os.path.join(myPath, myFile)

	with open(csvFile, 'w') as csv:
		csv.write("Column1, Column2, Column3 \n")
		x = 0
		y = 0
		value = 0
		value2 = 0
		while x < 5000:
			key = "Entry{}".format(y)
			csv.write("{},{},{} \n".format(key, value, value2))
			x = x+1
			y = y+1
			value = value+1




if __name__=="__main__":
	main()
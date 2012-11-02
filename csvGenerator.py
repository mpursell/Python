import os

def main():

	myPath = raw_input("Enter a path:  ")
	myFile = raw_input("Enter a filename:  ")
	csvFile = os.path.join(myPath, myFile)

	with open(csvFile, 'w') as csv:
		csv.write("Column1, Column2, Column3 \n") #Add column headings into this string

		#initialise some counter variables
		entries = 0 #csv entries counter
		y = 0
		value = 0
		value2 = 0
		while entries < 5000: #set the max number of entries here 
			key = "Entry{}".format(y) #set up first column variables as "key"
			csv.write("{},{},{} \n".format(key, value, value2)) #write out the lines
			#increment the counters
			entries = entries+1
			y = y+1
			value = value+1
			value2 = value2+1




if __name__=="__main__":
	main()
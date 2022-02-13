import models

# Convert data_object to data_string
def Object2String(dataType, dataValue_object):
	if dataType == "Double" or dataType == "Integer":
		return str(dataValue_object)
	elif dataType == "DoubleVector":
		dataValue_string = ','.join(str(e) for e in dataValue_object)
		return dataValue_string
	elif dataType == "DoubleMatrix":
		dataValue_string = ""
		for list in dataValue_object:
			str1 = ','.join(str(e) for e in list)
			dataValue_string = dataValue_string + str1 + ";"
		dataValue_string = dataValue_string[:-1]
		return dataValue_string

list1 = [[1, 2, 3], [4, 5, 6]]
str1 = ','.join(str(e) for e in list1)

dataValue_string = Object2String("DoubleMatrix", list1)

def GetDataObject(dataType, dataValue_string):
	if dataType == "Double":
		scalar_double = float(dataValue_string)
		return scalar_double
	elif dataType == "Integer":
		scalar_integer = int(dataValue_string)
		return scalar_integer
	elif dataType == "DoubleMatrix":
		array_list = dataValue_string.split(";")
		matrix_double = []
		for i in range(len(array_list)):
			matrix_double.append(list(map(float, array_list[i].split(","))))
		return matrix_double

# inputs
args = ()

dataValue_string = "1,2,3;4,5,6"
print("333")
print(dataValue_string)
if ";" in dataValue_string:
    dataValue_object = GetDataObject("DoubleMatrix", dataValue_string)
    args += (dataValue_object,)
elif "," in dataValue_string:
    dataValue_object = GetDataObject("DoubleVector", dataValue_string)
    args += (dataValue_object,)
else:
    dataValue_object = GetDataObject("Double", dataValue_string)
    args += (dataValue_object,)
print("--------------------------------")


vvv = "1,2,3;4,5,6"
array_list = vvv.split(";")
array2D = []
for i in range(len(array_list)):
    array2D.append(list(map(float, array_list[i].split(","))))


args = ()
args += ([1,2,3],)
args += (3,)
y1 = getattr(models, "ArrayModel")(*args)
x = 0

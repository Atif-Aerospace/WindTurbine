from flask import Blueprint, request, make_response, jsonify
import models

execute_models_api = Blueprint('execute_models_api', __name__)

@execute_models_api.route("/execute-model", methods=["POST"])
def ExecuteModels():
	if request.is_json:
		req_json = request.get_json()
		print(req_json)
		modelName = req_json.get("name")
		
		#print(req_json["ModelName"])
		print("Executing Model: " + modelName)

		# inputs
		args = ()
		for input in req_json["inputs"]:
			#print(str(input["name"]) + " = " + str(input["value"]))
			dataName = input["name"]
			dataType = input["type"]
			dataValue_string = input["value"]
			dataValue_object = GetDataObject(dataType, dataValue_string)
			args += (dataValue_object,)
		print("Model Inputs: ")
		print(args)
		
		# outputs
		outputs = ()
		for output in req_json["outputs"]:
			#print(str(output["name"]) + " = " + str(output["value"]))
			outputs += (output["value"],)
		

		# execution
		y1 = getattr(models, modelName)(*args)
		
		print("Model Outputs: ")
		print(y1)
		
		response_body = {
            "name": modelName,
			"inputs": [],
			"outputs": []
        }
		for input in req_json["inputs"]:
			response_body["inputs"].append({"name": input["name"], "value": input["value"]})
		for output in req_json["outputs"]:
			dataValue_string = Object2String(output["type"], y1)
			print("^^^^^^^^^^^^^^^^^^^^^^^")
			print(y1)
			response_body["outputs"].append({"name": output["name"], "value": dataValue_string})

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		print("Error")
		return make_response(jsonify({"message": "Request body must be JSON"}), 400)


# Convert data_string to data_object
def GetDataObject(dataType, dataValue_string):
	if dataType == "Double":
		double = float(dataValue_string)
		return double
	elif dataType == "Integer":
		integer = int(dataValue_string)
		return integer
	elif dataType == "DoubleVector":
		doubleVector = list(map(float, dataValue_string.split(",")))
		return doubleVector
	elif dataType == "DoubleMatrix":
		array_list = dataValue_string.split(";")
		doubleMatrix = []
		for i in range(len(array_list)):
			doubleMatrix.append(list(map(float, array_list[i].split(","))))
		return doubleMatrix


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
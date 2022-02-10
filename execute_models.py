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
			dataValue_string = input["value"]
			if ";" in dataValue_string:
				dataValue_object = GetDataObject("DoubleMatrix", dataValue_string)
				args += (dataValue_object,)
			elif "," in dataValue_string:
				dataValue_object = GetDataObject("DoubleVector", dataValue_string)
				args += (dataValue_object,)
			else:
				dataValue_object = GetDataObject("Double", dataValue_string)
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
			response_body["outputs"].append({"name": output["name"], "value": y1})

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		print("Error")
		return make_response(jsonify({"message": "Request body must be JSON"}), 400)



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



# def Object2String(dataType, dataValue_object):
# 	if dataType == "Double":

# 	elif dataType == "Integer":

# 	elif dataType == "DoubleVector":

# 	elif dataType == "DoubleMatrix":
# 	list1 = [1, 2, 3]
# 	str1 = ''.join(str(e) for e in list1)
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

import models

from execute_models import execute_models_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(execute_models_api)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/aircadia')
def aaa():
    return "Hello, AirCADia!"



# @app.route('/aaa/<name>/<location>')
# def createUser(name, location):
#     user = User(name = name, location = location)
#     db.session.add(user)
#     db.session.commit()
#     return '<h1>Added New User</h1>'


# @app.route('/bbb/<name>')
# def GetUser(name):
#     user = User.query.filter_by(name = name).first()
#     return f'<h1>The user is located in: {user.location}</h1>'

# @app.route('/ccc/<name>')
# def delete_user(name):
#     user = User.query.filter_by(name = name).first()
#     db.session.delete(user)
#     db.session.commit()
#     return f'<h1>The user is located in: {user.location}</h1>'

@app.route('/create-project', methods=["POST"])
def create_project():
    if request.is_json:
        req_json = request.get_json()
        key = req_json.get("key")
        value = req_json["value"]
        
        
        data = ProjectSetting(key=key, value=value)
        db.session.add(data)
        db.session.commit()

        response_body = {"Result": "Data Created"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

@app.route('/get-project', methods=["GET"])
def get_project():
    project = {}

    # project settings
    projectSettings = ProjectSetting.query.all()
    for projectSetting in projectSettings:
        key = projectSetting.key
        value = projectSetting.value
        if key == "name":
            project["name"] = value
        if key == "endPoint":
            project["endPoint"] = value

    # data
    dataList = []
    dataVariables = DataVariable.query.all()
    for dataVariable in dataVariables:
        data = {
            "name": dataVariable.name,
            "category": dataVariable.category,
            "description": dataVariable.description,
            "type": dataVariable.type,
            "value": dataVariable.value,
            "unit": dataVariable.unit,
            "minValue": dataVariable.minValue,
            "maxValue": dataVariable.maxValue,
        }
        dataList.append(data)
        print(dataVariable)
    project["data"] = dataList

    # models
    modelsList = []
    models = ComputationalModel.query.all()
    for computationalModel in models:
        model = {}
        model["name"] = computationalModel.name
        model["category"] = computationalModel.category
        model["description"] = computationalModel.description
        model["endPoint"] = computationalModel.endPoint
        modelInputs = []
        for input in computationalModel.inputs:
            modelInputs.append({"name": input.name})
        model["inputs"] = modelInputs
        modelOutputs = []
        for output in computationalModel.outputs:
            modelOutputs.append({"name": output.name})
        model["outputs"] = modelOutputs
        print(len(computationalModel.inputs))
        print(len(computationalModel.inputs))
        modelsList.append(model)
    project["models"] = modelsList

    # workflows
    workflowsList = []
    workflows = ComputationalWorkflow.query.all()
    for computationalWorkflow in workflows:
        workflow = {}
        workflow["name"] = computationalWorkflow.name
        workflow["category"] = computationalWorkflow.category
        workflow["description"] = computationalWorkflow.description

        # data objects
        dataObjects = []
        for input in computationalWorkflow.inputs:
            for data in dataList:
                if data["name"] == input.name:
                    dataObjects.append(data)
                    break
        for output in computationalWorkflow.outputs:
            for data in dataList:
                if data["name"] == output.name:
                    dataObjects.append(data)
                    break
        workflow["data"] = dataObjects

        # inputs
        modelInputs = []
        for input in computationalWorkflow.inputs:
            modelInputs.append({"name": input.name})
        workflow["inputs"] = modelInputs

        # outputs
        modelOutputs = []
        for output in computationalWorkflow.outputs:
            modelOutputs.append({"name": output.name})
        workflow["outputs"] = modelOutputs

        

        executableComponents = []
        for executableComponent in computationalWorkflow.executable_components:
            model = {}
            model["name"] = executableComponent.name
            model["category"] = executableComponent.category
            model["description"] = executableComponent.description
            model["endPoint"] = executableComponent.endPoint
            modelInputs = []
            for input in executableComponent.inputs:
                modelInputs.append({"name": input.name})
            model["inputs"] = modelInputs
            modelOutputs = []
            for output in executableComponent.outputs:
                modelOutputs.append({"name": output.name})
            model["outputs"] = modelOutputs
            executableComponents.append(model)
        workflow["executableComponents"] = executableComponents

        scheduledComponents = []
        for scheduledComponent in computationalWorkflow.scheduled_components:
            model = {}
            model["name"] = scheduledComponent.name
            model["category"] = scheduledComponent.category
            model["description"] = scheduledComponent.description
            model["endPoint"] = scheduledComponent.endPoint
            modelInputs = []
            for input in scheduledComponent.inputs:
                modelInputs.append({"name": input.name})
            model["inputs"] = modelInputs
            modelOutputs = []
            for output in scheduledComponent.outputs:
                modelOutputs.append({"name": output.name})
            model["outputs"] = modelOutputs
            scheduledComponents.append(model)
        workflow["scheduledComponents"] = scheduledComponents
        workflowsList.append(workflow)
    project["workflows"] = workflowsList

    # studies
    
    res = make_response(jsonify(project), 200)
    return res
    


@app.route('/create-data', methods=["POST"])
def create_data():
    if request.is_json:
        req_json = request.get_json()
        
        # create data for the given json
        _create_data(req_json)

        response_body = {"Result": "Data Created"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)
@app.route('/create-dataObjects', methods=["POST"])
def create_dataObjects():
    if request.is_json:
        req_json = request.get_json()
        
        for dataJson in req_json:
            # create data for the given json
            _create_data(dataJson)

        response_body = {"Result": "Data Created"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)
def _create_data(data_json):
    name = data_json.get("name")
    category = data_json.get("category")
    description = data_json.get("description")
    type = data_json["type"]
    value = data_json["value"]
    unit = data_json["unit"]
    minValue = data_json["minValue"]
    maxValue = data_json["maxValue"]
    
    # create database entry for "data variable" 
    data = DataVariable(name=name, category=category, description=description, type=type, value=value, unit=unit, minValue=minValue, maxValue=maxValue)
    db.session.add(data)
    db.session.commit()

@app.route('/delete-data', methods=["POST"])
def delete_data():
    if request.is_json:
        req_json = request.get_json()
        name = req_json.get("name")
        category = req_json.get("category")
        description = req_json.get("description")
        type = req_json["type"]
        value = req_json["value"]
        unit = req_json["unit"]
        minValue = req_json["minValue"]
        maxValue = req_json["maxValue"]
        
        # create database entry for "data variable"
        DataVariable.query.filter_by(name = name).delete()
        # data = DataVariable(name=name, category=category, description=description, type=type, value=value, unit=unit, minValue=minValue, maxValue=maxValue)
        # db.session.delete(data)
        db.session.commit()

        response_body = {"Result": "Data Deleted"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

@app.route('/create-model', methods=["POST"])
def create_model():
    if request.is_json:
        req_json = request.get_json()

        _create_model(req_json)

        response_body = {"Result": "Model Created"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"error": "Request body must be JSON"}), 400)
def _create_model(model_json):
    name = model_json.get("name")
    category = model_json.get("category")
    description = model_json.get("description")
    endPoint = model_json["endPoint"]
    inputs = model_json["inputs"]
    outputs = model_json["outputs"]
    
    # create database entry for "computational model"
    model = ComputationalModel(name=name, category=category, description=description, endPoint=endPoint)
    for i in range(0, len(inputs)):
        dataVariable = DataVariable.query.filter_by(name = inputs[i]["name"]).first()
        if dataVariable is None:
            return make_response(jsonify({"error": "Data variable '" + inputs[i]["name"] + "' not Present"}), 400)
        model.inputs.append(dataVariable)
    for i in range(0, len(outputs)):
        dataVariable = DataVariable.query.filter_by(name = outputs[i]["name"]).first()
        if dataVariable is None:
            return make_response(jsonify({"error": "Data variable '" + outputs[i]["name"] + "' not Present"}), 400)
        model.outputs.append(dataVariable)
    db.session.add(model)
    db.session.commit()

@app.route('/create-workflow', methods=["POST"])
def create_workflow():
    if request.is_json:
        print('Atifee')
        req_json = request.get_json()
        name = req_json.get("name")
        category = req_json.get("category")
        description = req_json.get("description")
        workflow_data_json = req_json["data"]
        inputs = req_json["inputs"]
        outputs = req_json["outputs"]
        executable_components = req_json["executableComponents"]
        scheduled_components = req_json["scheduledComponents"]
        print('Atif')
        # create database entry for "computational workflow"

        workflow = ComputationalWorkflow(name=name, category=category, description=description)
        
        for i in range(0, len(inputs)):
            dataVariable = DataVariable.query.filter_by(name = inputs[i]["name"]).first()
            if dataVariable is None:
                return make_response(jsonify({"error": "Data variable '" + inputs[i]["name"] + "' not Present"}), 400)
            workflow.inputs.append(dataVariable)
        for i in range(0, len(outputs)):
            dataVariable = DataVariable.query.filter_by(name = outputs[i]["name"]).first()
            if dataVariable is None:
                return make_response(jsonify({"error": "Data variable '" + outputs[i]["name"] + "' not Present"}), 400)
            workflow.outputs.append(dataVariable)
        for i in range(0, len(executable_components)):
            computationalModel = ComputationalModel.query.filter_by(name = executable_components[i]["name"]).first()
            if computationalModel is None:
                return make_response(jsonify({"error": "Computational Model '" + executable_components[i]["name"] + "' not Present"}), 400)
            workflow.executable_components.append(computationalModel)

        db.session.add(workflow)
        print(workflow)
        db.session.commit()

        response_body = {"Result": "Workflow Created"}
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"error": "Request body must be JSON"}), 400)






























# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(50))
#     location = db.Column(db.String(50))
#     #date_created = db.Column(db.DateTime, dafault = datetime.now)



# Table for storing project attributes
class ProjectSetting(db.Model):
    __tablename__ = 'ProjectSettings'
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(50))
    value = db.Column(db.String(50))

class DataVariable(db.Model):
    __tablename__ = 'DataVariables'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(50))
    type = db.Column(db.String(50))
    value = db.Column(db.String(50))
    unit = db.Column(db.String(50))
    minValue = db.Column(db.String(50))
    maxValue = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, dafault = datetime.now)
    #ComputationalModels = db.relationship("ComputationalModel", secondary="ModelInputs")


class ComputationalModel(db.Model):
    __tablename__ = 'ComputationalModels'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(50))
    endPoint = db.Column(db.String(50))
    #location = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, dafault = datetime.now)
    #inputs = db.relationship('Data', backref='owner')
    inputs = db.relationship("DataVariable", secondary="ModelInputs")
    outputs = db.relationship("DataVariable", secondary="ModelOutputs")


class ModelInput(db.Model):
    __tablename__ = 'ModelInputs'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ComputationalModels.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('DataVariables.id'))
    model = db.relationship(ComputationalModel, backref=db.backref("ModelInputs", cascade="all, delete-orphan"))
    data = db.relationship(DataVariable, backref=db.backref("ModelInputs", cascade="all, delete-orphan"))


class ModelOutput(db.Model):
    __tablename__ = 'ModelOutputs'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ComputationalModels.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('DataVariables.id'))
    model = db.relationship(ComputationalModel, backref=db.backref("ModelOutputs", cascade="all, delete-orphan"))
    data = db.relationship(DataVariable, backref=db.backref("ModelOutputs", cascade="all, delete-orphan"))


class ComputationalWorkflow(db.Model):
    __tablename__ = 'ComputationalWorkflows'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(500))
    #location = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, dafault = datetime.now)
    # inputs = db.Column(db.String(5000))
    # outputs = db.Column(db.String(5000))
    inputs = db.relationship("DataVariable", secondary="WorkflowInputs")
    outputs = db.relationship("DataVariable", secondary="WorkflowOutputs")
    executable_components = db.relationship("ComputationalModel", secondary="WorkflowExecutableComponents")
    scheduled_components = db.relationship("ComputationalModel", secondary="WorkflowScheduledComponents")


class WorkflowInput(db.Model):
    __tablename__ = 'WorkflowInputs'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('ComputationalWorkflows.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('DataVariables.id'))
    workflow = db.relationship(ComputationalWorkflow, backref=db.backref("WorkflowInputs", cascade="all, delete-orphan"))
    data = db.relationship(DataVariable, backref=db.backref("WorkflowInputs", cascade="all, delete-orphan"))


class WorkflowOutput(db.Model):
    __tablename__ = 'WorkflowOutputs'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('ComputationalWorkflows.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('DataVariables.id'))
    workflow = db.relationship(ComputationalWorkflow, backref=db.backref("WorkflowOutputs", cascade="all, delete-orphan"))
    data = db.relationship(DataVariable, backref=db.backref("WorkflowOutputs", cascade="all, delete-orphan"))


class WorkflowExecutableComponent(db.Model):
    __tablename__ = 'WorkflowExecutableComponents'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('ComputationalWorkflows.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('ComputationalModels.id'))
    workflow = db.relationship(ComputationalWorkflow, backref=db.backref("WorkflowExecutableComponents", cascade="all, delete-orphan"))
    model = db.relationship(ComputationalModel, backref=db.backref("WorkflowExecutableComponents", cascade="all, delete-orphan"))

class WorkflowScheduledComponent(db.Model):
    __tablename__ = 'WorkflowScheduledComponents'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('ComputationalWorkflows.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('ComputationalModels.id'))
    workflow = db.relationship(ComputationalWorkflow, backref=db.backref("WorkflowScheduledComponents", cascade="all, delete-orphan"))
    model = db.relationship(ComputationalModel, backref=db.backref("WorkflowScheduledComponents", cascade="all, delete-orphan"))

if __name__ == '__main__':
    app.run(debug=True, port=3002)
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

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

        
        dataObjects = []

        # inputs
        modelInputs = []
        for input in computationalWorkflow.inputs:
            modelInputs.append({"name": input.name})
            for data in dataList:
                if data["name"] == input.name:
                    dataObjects.append(data)
                    break
        workflow["inputs"] = modelInputs

        # outputs
        modelOutputs = []
        for output in computationalWorkflow.outputs:
            modelOutputs.append({"name": output.name})
            for data in dataList:
                if data["name"] == output.name:
                    dataObjects.append(data)
                    break
        workflow["outputs"] = modelOutputs

        # data objects
        workflow["data"] = dataObjects

        executableComponents = []
        for executableComponent in computationalWorkflow.executable_components:
            executableComponents.append({"name": executableComponent.name})
        workflow["executable-components"] = executableComponents

        scheduledComponents = []
        for scheduledComponent in computationalWorkflow.scheduled_components:
            scheduledComponents.append({"name": scheduledComponent.name})
        workflow["scheduled-components"] = scheduledComponents
        workflowsList.append(workflow)
    project["workflows"] = workflowsList

    # studies
    
    res = make_response(jsonify(project), 200)
    return res















app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.db'
db = SQLAlchemy(app)






























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



get_project()
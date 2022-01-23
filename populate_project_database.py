from app import *
db.create_all()

# project settings
s1 = ProjectSetting(key='name', value='Wind Turbine')
db.session.add(s1)
s2 = ProjectSetting(key='endPoint', value='http://127.0.0.1:5000/')
db.session.add(s2)


# data variables
x1 = DataVariable(name='x1', category='system.test', description='First data variable', type='Double', value='2.0', unit='ft', minValue='0.0', maxValue='100.0')
db.session.add(x1)
x2 = DataVariable(name='x2', category='system.test', description='Second data variable', type='Double', value='3.0', unit='ft', minValue='0.0', maxValue='100.0')
db.session.add(x2)
y1 = DataVariable(name='y1', category='system.test', description='Third data variable', type='Double', value='0.0', unit='ft', minValue='0.0', maxValue='100.0')
db.session.add(y1)
y2 = DataVariable(name='y2', category='system.test', description='Fourth data variable', type='Double', value='0.0', unit='ft', minValue='0.0', maxValue='100.0')
db.session.add(y2)

# models
m1 = ComputationalModel(name='AddNumbers', category='system.test', description='Calculates the addition of two numbers', endPoint='http://127.0.0.1:5000/execute-model')
m1.inputs.append(x1)
m1.inputs.append(x2)
m1.outputs.append(y1)
db.session.add(m1)


# workflows
wf1 = ComputationalWorkflow(name='WF1', category='system.test', description='First Workflow', inputs='x1,x2', outputs='x1,x2', executable_components='x1,x2', scheduled_components='x1,x2')
db.session.add(wf1)

db.session.commit()


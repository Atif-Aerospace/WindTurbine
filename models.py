import os, subprocess

def AddNumbers(x1, x2):
    return (x1 + x2)

def MultiplyNumbers(x1, x2):
	return (x1 * x2)

def TwoOutputsModel(x1, x2):
	y1 = x1 + x2
	y2 = x1 * x2
	return (y1, y2)

def ArrayModel(array, scalar):
    array[0] = scalar
    y = array
    return (y)

def FlopsModel(x1, x2):
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())

    os.chdir('flops')

    # ==================
    # Step 1: set inputs
    # ==================

    a_file = open("xAtif.in", "r")
    list_of_lines = a_file.readlines()
    a_file.close()

    # thickness 1
    thickness1 = "{:.2f}".format(x1)
    line = list_of_lines[17]
    line = line.replace(line[5:12], str(thickness1))
    list_of_lines[17] = line

    a_file = open("xAtif_new.in", "w")
    a_file.writelines(list_of_lines)
    a_file.close()


    # =========================
    # Step 2: execute .exe file
    # =========================

    subprocess.call(["xAtif.bat"])

    # ===================
    # Step 3: get outputs
    # ===================

    a_file = open("xAtif.out", "r")
    list_of_lines = a_file.readlines()
    a_file.close()

    # weight
    lineNumber = -1
    for i in range(len(list_of_lines)):
        if '#OBJ/VAR/CONSTR SUMMARY' in list_of_lines[i]:
            lineNumber = i
            break

    lll = list_of_lines[lineNumber + 3]
    stringOutput = lll[11:17]
    output = float(lll[11:17])

    y1 = output
    
    return (y1)
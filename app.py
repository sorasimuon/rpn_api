from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app)
BASE_URL = r'/rpn/'

list_stacks = {}

def isValidNumber(value):
    """
    Check validity of the number format
    return: True or False
    """
    if type(value) == str:
        regex = re.compile(r'^[0-9]*[.]?[0-9]+$')

        if regex.match(value):
            return True
        else:
            return False
    
    elif type(value) in [int, float]:
        return True

def isOperator(value):
    """
    check if it is a valid operand
    return: True or False
    """
    return (True if (re.match(r'^[+\-*/]$', value) != None) else False)
    
def getAvailableIdStack():
    """
    Get the first id available (not part of list_stack keys)
    output: int id_stack
    """
    id_stack = 0

    while id_stack in list_stacks.keys():
        id_stack += 1
    return id_stack
    

@app.route(BASE_URL + 'stack', methods=['POST'])
def createNewStack():
    """
    Create a new Stack and add it to the list of stacks
    return: newly created stack
    """
    id = getAvailableIdStack() 
    list_stacks[id] = []
    print(list_stacks)
    return make_response(jsonify({"_id":id,"stack":list_stacks[id]}), 201)

@app.route(BASE_URL + 'stack', methods=['GET'])
def getListStack():
    """
    Retrieve the entire list of stacks
    output: the list of stacks
    """
    result = []
    if len(list_stacks) > 0:
        for key, value in list_stacks.items():
            result.append({"_id":key, "stack":value})
    return make_response (jsonify(result),200)
        

@app.route(BASE_URL + 'stack/<id>', methods=['GET'])
def getStack(id):
    """
    Retrieve and send back the desired stack 
    input : Id of the Stack
    output: the desired stack
    """
    id = int(id)
    if id in list_stacks.keys():
        return make_response(jsonify({"_id": id, "stack": list_stacks[id]}), 200)
    else:
        return make_response('Stack id not defined', 400)
    
@app.route(BASE_URL + '/stack/<id>', methods=['DELETE'])
def deleteStack(id):
    id = int(id)
    if id in list_stacks.keys():
        list_stacks.pop(id)
        print(list_stacks)
        result = []
        if len(list_stacks) > 0:
            for key, value in list_stacks.items():
                result.append({"_id":key, "stack":value})
        return make_response (jsonify(result),200)
    else:
        return make_response("stack {} does not exist".format(id), 400)

@app.route(BASE_URL + 'stack/<id>', methods=['POST'])
def addValue(id):
    id = int(id)
    value = request.json['value']
    if id in list_stacks.keys():
        if isValidNumber(value):
            list_stacks[id].append(float(value))
            print(list_stacks[id])
            return make_response(jsonify({"_id": id, "stack": list_stacks[id]}), 200)
        else:
            return make_response('Error : Input not a number'.format(id), 400)
    else:
        return make_response('Stack {} does not exist'.format(id), 400)

@app.route(BASE_URL + '/op/stack/<id>', methods=['POST'])
def calculate(id):
    id = int(id)
    operator = request.json['operator']
    try:  
        if isOperator(operator):
            if id in list_stacks.keys():
                if len(list_stacks[id]) > 1:
                    secondOperand = list_stacks[id].pop()
                    firstOperand = list_stacks[id].pop()
                    result = eval("{}{}{}".format(str(firstOperand), operator, str(secondOperand)))
                    print("{}{}{}".format(str(firstOperand), operator, str(secondOperand)))
                    print(result)
                    list_stacks[id].append(result)
                    print(list_stacks[id])
                return make_response(jsonify({"_id": id, "stack": list_stacks[id]}), 200)
            else:
                return make_response("stack {} does not exist".format(id), 400)
        else:
            return make_response("Operator not valid", 400)
    except ZeroDivisionError:
        return make_response('Error: Division by zero not valid', 400)

if __name__ == "__main__":

    app.run()

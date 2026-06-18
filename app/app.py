import os, uuid, boto3
from flask import Flask, jsonify, request

app = Flask(__name__)
table = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1")) \
             .Table(os.environ.get("DYNAMODB_TABLE", "tasks"))

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(table.scan()["Items"])

@app.route("/tasks", methods=["POST"])
def create_task():
    item = {"id": str(uuid.uuid4()), "title": request.json["title"], "status": "pending"}
    table.put_item(Item=item)
    return jsonify(item), 201

@app.route("/tasks/<id>", methods=["PUT"])
def update_task(id):
    body = request.json
    table.update_item(Key={"id": id},
        UpdateExpression="SET title=:t, #s=:s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":t": body["title"], ":s": body["status"]})
    return jsonify({"id": id, **body})

@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    table.delete_item(Key={"id": id})
    return "", 204

app.run(host="0.0.0.0", port=5000)

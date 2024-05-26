from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuration for MySQL database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Happyeveryday0519**"
app.config["MYSQL_DB"] = "finalproj"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

app.config["JWT_SECRET_KEY"] = "1A2b3C4d5E"
jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username == "admin" and password == "helloworld":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route("/persons", methods=["GET"])
@jwt_required()
def get_persons():
    data = data_fetch(""" SELECT * FROM persons """)
    return make_response(jsonify(data), 200)

@app.route("/persons", methods=["POST"])
@jwt_required()
def add_persons():
    cur = mysql.connection.cursor()
    info = request.get_json()

    name = info["Name"]
    age = info["Age"]
    email = info["Email"]

    cur.execute(
        """
            INSERT INTO persons (Age, Email, Name) VALUES (%s, %s, %s)
    """,
        (age, email, name),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "person added successfully", "rowsaffected": rows_affected}
        ),
        201,
    )

@app.route("/persons/<int:id>", methods=["GET"])
@jwt_required()
def get_persons_by_id(id):
    data = data_fetch(""" SELECT * FROM persons WHERE personid = {} """.format(id))
    return make_response(jsonify(data), 200)

@app.route("/persons/<int:id>", methods=["PUT"])
@jwt_required()
def update_person(id):
    cur = mysql.connection.cursor()
    info = request.get_json()

    name = info["Name"]
    age = info["Age"]
    email = info["Email"]

    cur.execute(
        """
        UPDATE persons SET Age = %s, Email = %s, Name = %s WHERE personid = %s
    """,
        (age, email, name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "person updated successfully", "rowsaffected": rows_affected}
        ),
        200,
    )

@app.route("/persons/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_persons(id):
    cur = mysql.connection.cursor()
    cur.execute(
        """
        DELETE FROM persons WHERE personid= %s
    """,
        (id,),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "person deleted successfully", "rowsaffected": rows_affected}
        ),
        200,
    )

@app.route("/persons/format", methods=["GET"])
@jwt_required()
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')

    return make_response(jsonify({"format": fmt, "foo": foo}), 200)

if __name__ == "__main__":
    app.run(debug=True)

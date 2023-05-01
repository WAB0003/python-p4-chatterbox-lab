from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

#Get messages
#Post messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    #!HANDLE GET ALL MESSAGES
    all_messages = Message.query.all()
    if request.method == "GET":
        message_list = [message.to_dict() for message in all_messages]
        
        response = make_response(jsonify(message_list), 200)
        return response        
    #!HANDLE POST NEW MESSAGE TO ALL MESSAGES   
    elif request.method == "POST":
        data = request.get_json()
        
        new_message = Message(
            username = data["username"],
            body = data["body"],
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return make_response(new_message.to_dict(), 201)
        
#Patch messages
#Delete messages
@app.route('/messages/<int:id>', methods = ["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()  
    #!HANDLE PATCH MESSAGE
    if request.method == 'PATCH':
        message_data = request.get_json()
        for attr in message_data:
            setattr(message, attr,message_data[attr])
        
        db.session.add(message)
        db.session.commit()
        
        response = make_response(message.to_dict(), 200)
        return response
        
    #!HANDLE DELETE MESSAGE
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response = make_response("Delete successful", 200)
        return response
    

if __name__ == '__main__':
    app.run(port=5555)

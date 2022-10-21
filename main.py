import json
from flask import Flask
from flask import request, redirect, jsonify
import datetime

app = Flask(__name__)
chat = list([])


def set_links(obj_id=None):
    adding = []
    chat_links = [
        {
            "href": "127.0.0.1/chat/show",
            "rel": "all",
            "type": "GET"
        },
        {
            "href": "127.0.0.1/chat/create",
            "rel": "add",
            "type": "POST"
        }
    ]
    if obj_id is not None:
        adding = [
            {
                "href": f"127.0.0.1/chat/show/{obj_id}",
                "rel": "message",
                "type": "GET"
            },
            {
                "delete": f"127.0.0.1/chat/delete/{obj_id}",
                "rel": "self",
                "type": "DELETE"
            },
            {
                "put": f"127.0.0.1/chat/put/{obj_id}",
                "rel": "self",
                "type": "PUT"
            }
        ]

    chat_links.extend(adding)
    return chat_links


def counter():
    counter.id += 1
    return str(counter.id)


counter.id = 0


def add_msg(text):
    msg = {
        "id": counter(),
        "text": text
    }
    chat.append(msg)


def create_hateoas_response(obj):
    if isinstance(obj, list):
        links = set_links()
    else:
        links = set_links(obj["id"])

    result = {
        "data": obj,
        "links": links
    }
    return jsonify(result)


add_msg("test")
add_msg("second test")


@app.route('/')
def index():
    return 'Welcome to my page'


@app.route('/chat/show', methods=['GET'])
def show_all_chats():
    return create_hateoas_response(chat)


@app.route('/chat/show/<id>', methods=['GET'])
def show_chat_by_id(id):
    obj = None
    for x in chat:
        if x["id"] == id:
            obj = x
            break
    return create_hateoas_response(obj)


@app.route('/chat/create', methods=['POST'])
def create_chat():
    message = request.args.get("message")
    add_msg(message)
    obj = chat[-1]

    return create_hateoas_response(obj)


@app.route('/chat/delete/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    obj = None
    for x in chat:
        if x["id"] == chat_id:
            chat.remove(x)
            obj = x
            break

    return create_hateoas_response(obj)


@app.route('/chat/put/<chat_id>', methods=['PUT'])
def put_into_chat(chat_id):
    message = request.args.get("message")
    obj = None
    for x in chat:
        if x["id"] == chat_id:
            x["text"] = message
            obj = x
            break

    return create_hateoas_response(obj)


@app.route('/chat/doc')
def show_doc():
    text = "<div style=\"display: flex; flex-direction: column; align-items: center;\">" \
                "<h1>" \
                    "RESTAPI chat documentation" \
                "</h1>" \
                "<div>" \
                    "<strong>/chat/show(GET)</strong> - return all messages in chat with json response<br>" \
                    "<strong>/chat/show/<chat_id>(GET)</strong> - return message by id with json response<br>" \
                    "<strong>/chat/create(POST)</strong> - create and add message to chat by json request with \"message\" key (ex: {\"message\":\"<your text>\"})<br>" \
                    "<strong>/chat/delete/<chat_id>(DELETE)</strong> - delete message from chat by id<br>" \
                    "<strong>/chat/put/<chat_id>(PUT)</strong> - update message in chat by id" \
                "<div>" \
           "<div>"

    return text



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)

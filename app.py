from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, json, Response, jsonify,escape
from libs import *
import time
from config import *
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")



@app.route("/api/search/",methods=['GET'])
def json_search():
    """
    搜索接口
    """
    query = request.args.get('query')

    # one=get_ner_one(query)
    items=[]
    for it in search_sent_plus(query):
        print(it)
        items.append({'data': {"title":it.content,'content':it.content},'type':"item"})
    # emit('更新实体', {'data': one,'type':"item"})

    return jsonify({'datas':items})


@socketio.on('demo', namespace='/tapi')
def demo(message):
    """
    构建训练数据
    """
    print('message',message)
    keyword = message.get('data')
    while  True:
        emit('demo response', {'do': "start"})

        for it in search_sent_plus("柯基犬"):
            # emit('demo response', {'data': time.time()})
            # print()
            emit('demo response', {'data': it.content})
            time.sleep(1)


@socketio.on('submit_marked', namespace='/tapi')
def submit_marked(message):
    """
    构建训练数据
    """
    print('message',message)
    kgs=[]
    for marded in message.get('marked').split("\n"):
        kg=marded.split("||")
        kgs.append(kg)

    data={"sentence":message.get('text').strip(),'kgs':kgs}

    try:
        DB.kg_marked.insert_one(data)
        # DB.train.insert_one(data)
        emit('submit_marked response', {'msg': "success"})
        pass
    except :
        emit('submit_marked response', {'msg': "faill "})
        pass

@socketio.on('pre_mark', namespace='/tapi')
def pre_mark(message):
    """
    加载预先预测的和使用模型进行预测
    """
    print('pre_mark message',message)
    print("sentence",{"sentence":message.get("text").get("data")})
    kgs=[]
    for it in DB.kg_marked.find({"sentence":message.get("text").get("data").strip()}):
        # print(it)
        kgs=kgs+it["kgs"]
    if len(kgs)>0:
        print("加载之前标记数据")
    emit('pre_mark response', {'kgs': kgs})
    

    



    # kgs=[]
    # for marded in message.get('marked').split("\n"):
    #     kg=marded.split("||")
    #     kgs.append(kg)

    # data={"sentence":message.get('text'),'kgs':kgs}

    # try:
    #     DB.kg_marked.insert_one(data)
    #     # DB.train.insert_one(data)
    #     emit('submit_marked response', {'msg': "success"})
    #     pass
    # except :
    #     emit('submit_marked response', {'msg': "faill "})
    #     pass






if __name__ == "__main__":
    # app.run()
    # socketio.run(app)
    socketio.run(app, host="0.0.0.0", port=5000)
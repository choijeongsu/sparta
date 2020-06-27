from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('hometraining.html')


@app.route('/api/list', methods=['GET'])
def stars_list():
    stars = list(db.myyou.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'result': 'success', 'like_list': stars})


@app.route('/api/like', methods=['POST'])
def star_like():
    like_id = request.form['like_give']
    star = db.myyou.find_one({'name': like_id})
    if star == None:
        doc = {
            'name': like_id,
            'like': 1
        }
        db.myyou.insert_one(doc)
        
    else:
        new_like = star['like'] + 1
        db.myyou.update_one({'name': like_id}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('localhost', port=5002, debug=True)


from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('20200530_homework_week4.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_review():
    # 1. 클라이언트가 준 title, author, review 가져오기.
    # title_receive로 클라이언트가 준 title 가져오기
    name_receive = request.form['name_give']
    color_receive = request.form['color_give']
    number_receive = request.form['number_give']
    address_receive = request.form['address_give']
    tel_receive = request.form['tel_give']

	# 2. DB에 정보 삽입하기
    order = {
       'name': name_receive,
       'color': color_receive,
       'number': number_receive,
       'address': address_receive,
       'tel': tel_receive,

    }

    print("print-write_review",order)
    # reviews에 review 저장하기
    db.orders.insert_one(order)
    return jsonify({'result':'success', 'msg': '주문이 완료되었습니다'})

@app.route('/orders', methods=['GET'])
def read_orders():
    # 1. 모든 reviews의 문서를 가져온 후 list로 변환합니다.
    orders = list(db.orders.find({},{'_id':0}))
	# 2. 성공 메시지와 함께 리뷰를 보냅니다.
    return jsonify({'result':'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
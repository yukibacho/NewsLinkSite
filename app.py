from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import request

from DataStore.MySQLClient import MySQLClient
import news_scraping

dns = {
    'user': 'root',
    'host': 'localhost',
    'password':'mysql',
    'database': 'mysql',
    'use_unicode':'True',
	'charset':'utf8'
}
db = MySQLClient(**dns)

# Webページとしてのルーティングルール
app = Flask(__name__)

# ------------------------------------------------------------------
@app.route("/")
def main():
    props = {'title': 'News Topics', 'msg': 'News Topics'}
    stmf = 'SELECT * FROM NEWS_TBL ORDER BY ID ASC'
    topics = db.query(stmf)
    f = open('updatetime.txt')
    time = f.read();
    html = render_template('index.html', props=props, topics=topics, time=time)
    return html

@app.route('/api/udnews/<user>/<password>', methods=["POST","GET"])
def update_news(user,password):
    news_scraping.getnews(user,password)
    return redirect(url_for('main'))

@app.route('/api/news', methods=["GET"])
def all_news_get():
    stmf = 'SELECT * FROM NEWS_TBL ORDER BY ID ASC'
    topics = db.query(stmf)
    topicsj = [{
        'ID':topic[0],
        'title':topic[1],
        'link':topic[2]
    }for topic in topics]
    json = {
        'topics':topicsj
    }
    return jsonify(json)

@app.route('/api/news/<int:id>', methods=["GET"])
def news_get():
    stmf = 'SELECT * FROM NEWS_TBL WHERE ID =' + str(id)
    topic = db.query(stmf)
    json = {
        'ID':topic[0][0],
        'title':topic[0][1],
        'link':topic[0][2]
    }
    return jsonify(json)

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))

# ------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
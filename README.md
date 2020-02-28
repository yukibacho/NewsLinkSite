# NewsLinkSite

## はじめに
このプロジェクトでは、[yahooニューストップページ](https://news.yahoo.co.jp/)から主要ニュース一覧をwebスクレイピングで取得し、Webページにリンクを表示します。<br>
言語はPython、フレームワークはFlask、DBはDockerの公式Mysqlイメージを使用しています。<br>

## DockerのMYSQLコンテナのDBの文字コードの変更方法
①powershellで以下のコマンドを実行
>$docker container cp "Cloneしたディレクトリ"\newslinksite\my.cnf mysql:/etc/mysql/my.cnf

②コンテナを再起動
>$docker restart mysql

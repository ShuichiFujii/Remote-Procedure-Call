# Remote Procedure Call

## 概要

RPCは、ネットワーク上で接続された他のコンピュータのプログラムを呼び出し/実行するためのプロトコルである。本プログラムでは、UNIXドメインソケットを介して通信を行う。クライアントであるJavaScript側から、サーバ側のPythonへRPCリクエストをJSON形式で送信を行い、下記の関数を実行する。

### サーバー側の関数一覧
1. floor(x): 小数xを切り捨て整数型を返す
2. nroot(n, x): xの1/n乗根を求める
3. reverse(s): 文字列sを受け取り、反転して返す
4. validAnagram(s1, s2): 文字列s1, s2がアナグラムか判定する
5. sort(strArr): 文字列strArrを昇順ソート

### システム構成
サーバー及びクライアントは以下のように動作する。
- サーバー（Python）:
  - `RPCServer`クラスが`Functions`クラス内の関数をリモート実行
  - UNIXドメインソケット`/tmp/rpc.sock`を使用
  - `json`を用いてリクエスト処理
 
- クライアント（JavaScript / Node.js）:
  - `net.createConnection()`で`/tmp/rpc.sock`に接続
  - `JSON.stringify()`でリクエスト送信
  - サーバーのレスポンスを受け取る
 

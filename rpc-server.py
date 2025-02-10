import json
import socket
import os
import math

class Functions:
    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)
        
    @staticmethod
    def nroot(n: int, x: float) -> float:
        return x ** (1 / n)
    
    @staticmethod
    def reverse(s: str) -> str:
        return s[::-1]
    
    @staticmethod
    def validAnagram(s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

    @staticmethod
    def sort(strArr: str) -> str:
        return sorted(strArr)
    

class RPCServer:
    FUNCTION_MAP = {
        "floor": Functions.floor,
        "nroot": Functions.nroot,
        "reverse": Functions.reverse,
        "validAnagram": Functions.validAnagram,
        "sort": Functions.sort
    }
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = '/tmp/rpc.sock'
        
        # 既にファイルが作成されている場合は削除する
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        
        # アドレスの紐づけ
        self.sock.bind(self.server_address)
        
        # 接続待ち
        self.sock.listen(1)
        
        print(f"サーバーが立ち上がりました。 : {self.server_address}")
        
    def server_run(self):
        while True:
            connection, _ = self.sock.accept()
            print("🟡 クライアントが接続しました")
            self.handle_client(connection)
            
    def handle_client(self, connection):
        # リクエストを処理する。
        try:
            while True:
                data = connection.recv(4096)
                
                if not data:
                    break
                
                data_str = data.decode()
                
                print("🟢リクエストを受信しました\n")
                print(f"受信したデータ: {data_str}")
                
                response = self.process_request(data_str)
                connection.sendall((json.dumps(response) + "\n").encode('utf-8'))
                
        except Exception as e:
            print(f"エラーが発生しました。: {e}")
            
        finally:
            connection.close()
            print("🔴クライアントが切断されました")
            
            
    def process_request(self, data_str: str) -> dict:
        # リクエストを処理する
        try:
            request = json.loads(data_str.strip())
            print(f"リクエスト: {request}")
            
        except json.JSONDecodeError:
            return {
                "error": "無効なJSON形式です",
                "id": None
            }
        
        method = request.get("method")
        params = request.get("params", [])
        request_id = request.get("id", None)
        
        if method in self.FUNCTION_MAP:
            # メソッドが存在する場合
            result = self.FUNCTION_MAP[method](*params)
            
            response = {
                "result": result,
                "result_type": type(result).__name__,
                "id": request_id
            }
            
        else:
            # メソッドが存在しない場合
            response = {
                "error": f"メソッド '{method}' は未定義です",
                "id": request_id
            }
        
        return response
    
if __name__ == "__main__":
    rpc_server = RPCServer()
    rpc_server.server_run()
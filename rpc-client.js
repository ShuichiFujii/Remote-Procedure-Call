const net = require("net");

const SOCKET_PATH = "/tmp/rpc.sock";

// JSONリクエストの作成
const request = {
    "method": "nroot",
    "params": [27, 3],
    "param_types": ["int", "int"],
    "id": 1
};

const client = net.createConnection(SOCKET_PATH, () => {
    console.log("🟢 サーバーに接続しました");
    client.write(JSON.stringify(request) + "\n");
})

// データ受信時の処理
client.on("data", (data) => {
    console.log("📥サーバからのレスポンス: " + data.toString().trim());
    client.end();
})

client.on("error", (err) => {
    console.error("🔴 エラー:", err.message);
});

client.on("end", () => {
    console.log("🔴 サーバーとの接続が終了しました");
})
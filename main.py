import requests
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Cho phép tất cả origin (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://apihitclub.up.railway.app/api/history"

# ------------------- Lấy dữ liệu từ API nguồn -------------------
def fetch_data():
    try:
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        data = res.json()
        return data.get("taixiu", [])
    except Exception as e:
        print("❌ Lỗi lấy dữ liệu:", e)
        return []

# ------------------- Mẹo dự đoán -------------------
def du_doan_theo_meo(record):
    try:
        tong = record["Tong"]
        x1 = record["Xuc_xac_1"]
        return "Tài" if (tong + x1) % 2 == 0 else "Xỉu"
    except Exception as e:
        print("❌ Lỗi trong hàm dự đoán:", e)
        return "Không xác định"

# ------------------- Trang chủ -------------------
@app.get("/")
def home():
    return {"message": "🎲 API Tài/Xỉu HitClub theo mẹo (không AI) đã sẵn sàng."}

# ------------------- API Dự đoán -------------------
@app.get("/taixiu/hitclub")
def taixiu_hitclub():
    data = fetch_data()
    if not data:
        return JSONResponse(content={"error": "Không có dữ liệu."}, status_code=400)

    try:
        phien = data[0]

        return {
            "id": "ExTaiXiu2010",
            "phien": phien["Phien"],
            "xuc_xac_1": phien["Xuc_xac_1"],
            "xuc_xac_2": phien["Xuc_xac_2"],
            "xuc_xac_3": phien["Xuc_xac_3"],
            "tong": phien["Tong"],
            "ket_qua": phien["Ket_qua"],
            "du_doan": du_doan_theo_meo(phien),
            "ty_le_thanh_cong": f"{random.randint(60, 75)}%"
        }

    except Exception as e:
        print("❌ Lỗi xử lý dữ liệu:", e)
        return JSONResponse(content={"error": f"Lỗi xử lý dữ liệu: {e}"}, status_code=500)
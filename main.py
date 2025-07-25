import requests
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

API_URL = "https://apihitclub.up.railway.app/api/history"

# ------------------- Lấy dữ liệu -------------------
def fetch_data():
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()
        return data.get("taixiu", [])
    except Exception as e:
        print("❌ Lỗi khi lấy dữ liệu:", e)
        return []

# ------------------- Dự đoán theo mẹo -------------------
def du_doan_theo_meo(record):
    try:
        tong = record["Tong"]
        x1 = record["Xuc_xac_1"]
        return "Tài" if (tong + x1) % 2 == 0 else "Xỉu"
    except:
        return "Không xác định"

# ------------------- API Trang chủ -------------------
@app.get("/")
def home():
    return {"message": "🎲 API Tài/Xỉu HitClub theo mẹo (không AI) đã sẵn sàng."}

# ------------------- API Dự đoán -------------------
@app.get("/taixiu/hitclub")
def taixiu_hitclub():
    data = fetch_data()
    if not data:
        return JSONResponse(content={"error": "Không có dữ liệu."}, status_code=400)

    phien = data[0]  # phiên mới nhất

    try:
        session = phien["Phien"]
        dice_1 = phien["Xuc_xac_1"]
        dice_2 = phien["Xuc_xac_2"]
        dice_3 = phien["Xuc_xac_3"]
        result = phien["Ket_qua"]
        du_doan = du_doan_theo_meo(phien)

        # Random tỉ lệ tin tưởng từ 70 đến 90%
        ti_le = f"{random.randint(70, 90)}%"

        return {
            "current_session": session,
            "dice_1": dice_1,
            "dice_2": dice_2,
            "dice_3": dice_3,
            "result": result,
            "next_session": session + 1,
            "du_doan": du_doan,
            "ti_le": ti_le,
            "Admin_1": "ĐÔNG DƯƠNG",
            "Admin_2": "MR SIMON"
        }
    except Exception as e:
        return JSONResponse(content={"error": f"Lỗi xử lý dữ liệu: {e}"}, status_code=500)
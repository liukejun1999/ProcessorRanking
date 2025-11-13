from pathlib import Path
import json
from datetime import datetime
# 导入新的爬虫模块
from . import cpuranklist

base_dir = Path(__file__).resolve().parents[2] / "data"

def write(name: str, payload: dict):
    base_dir.mkdir(parents=True, exist_ok=True)
    tmp = base_dir / (name + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    tmp.replace(base_dir / name)

def mobile():
    items = [
        {"id":"apple-a17","name":"Apple A17 Pro","brand":"Apple","cpu_arch":"Armv9","gpu_arch":"Apple","process_nm":3,"release_year":2023,"score_cpu":2900,"score_gpu":12000,"score_total":15000,"tdp_w":6,"efficiency":2500},
        {"id":"snapdragon-8gen3","name":"Qualcomm Snapdragon 8 Gen 3","brand":"Qualcomm","cpu_arch":"Armv9","gpu_arch":"Adreno","process_nm":4,"release_year":2023,"score_cpu":2300,"score_gpu":9000,"score_total":11300,"tdp_w":6,"efficiency":1883},
        {"id":"dimensity-9300","name":"MediaTek Dimensity 9300","brand":"MediaTek","cpu_arch":"Armv9","gpu_arch":"Immortalis","process_nm":4,"release_year":2023,"score_cpu":2400,"score_gpu":9500,"score_total":11900,"tdp_w":7,"efficiency":1700}
    ]
    payload = {"items": items, "total": len(items), "updated_at": datetime.utcnow().isoformat(), "source": ["seed"]}
    write("mobile-soc.json", payload)

def cpu():
    items = [
        {"id":"i9-14900k","name":"Intel Core i9-14900K","brand":"Intel","cores":24,"threads":32,"base_clk":3.2,"boost_clk":6.0,"process_nm":10,"tdp_w":125,"release_year":2023,"score_single":2200,"score_multi":20000,"efficiency":160},
        {"id":"ryzen-9-7950x","name":"AMD Ryzen 9 7950X","brand":"AMD","cores":16,"threads":32,"base_clk":4.5,"boost_clk":5.7,"process_nm":5,"tdp_w":170,"release_year":2022,"score_single":2100,"score_multi":18500,"efficiency":109},
        {"id":"i7-13700k","name":"Intel Core i7-13700K","brand":"Intel","cores":16,"threads":24,"base_clk":3.4,"boost_clk":5.4,"process_nm":10,"tdp_w":125,"release_year":2022,"score_single":1900,"score_multi":16000,"efficiency":128}
    ]
    payload = {"items": items, "total": len(items), "updated_at": datetime.utcnow().isoformat(), "source": ["seed"]}
    write("pc-cpu.json", payload)

def gpu():
    items = [
        {"id":"rtx-4090","name":"NVIDIA GeForce RTX 4090","brand":"NVIDIA","vram_gb":24,"process_nm":4,"tdp_w":450,"release_year":2022,"score_3d":10000,"efficiency":22},
        {"id":"rx-7900xtx","name":"AMD Radeon RX 7900 XTX","brand":"AMD","vram_gb":24,"process_nm":5,"tdp_w":355,"release_year":2022,"score_3d":8500,"efficiency":24},
        {"id":"rtx-4080","name":"NVIDIA GeForce RTX 4080","brand":"NVIDIA","vram_gb":16,"process_nm":4,"tdp_w":320,"release_year":2022,"score_3d":8000,"efficiency":25}
    ]
    payload = {"items": items, "total": len(items), "updated_at": datetime.utcnow().isoformat(), "source": ["seed"]}
    write("pc-gpu.json", payload)

def run(target: str):
    # 优先使用新的爬虫模块
    try:
        # 调用新爬虫模块的run函数
        cpuranklist.run(target)
        print(f"已使用新爬虫模块更新 {target} 数据")
    except Exception as e:
        print(f"新爬虫模块执行失败: {str(e)}，回退到默认数据")
        # 如果新爬虫失败，回退到原来的方法
        if target == "mobile":
            mobile()
        elif target == "cpu":
            cpu()
        elif target == "gpu":
            gpu()
        elif target == "all":
            mobile(); cpu(); gpu()
        meta = {"updated_at": datetime.utcnow().isoformat(), "source": ["seed"], "version": "0.0.1"}
        write("meta.json", meta)

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.scrapers.cpuranklist import (
    fetch_html,
    scrape_cpu_rankings,
    scrape_gpu_rankings,
    scrape_mobile_soc_rankings,
    write,
    update_mobile_soc,
    update_cpu,
    update_gpu,
    run
)


def test():
    # 测试CPU排行榜解析
    results = scrape_cpu_rankings()
    print(f"CPU排行榜结果: {results}")

    # # 测试GPU排行榜解析
    # results = scrape_gpu_rankings()
    # print(f"GPU排行榜结果: {results}")

    # # 测试移动SoC排行榜解析
    # results = scrape_mobile_soc_rankings()
    # print(f"移动SoC排行榜结果: {results}")


if __name__ == '__main__':
    test()
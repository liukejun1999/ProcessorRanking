# 处理器排行榜 H5 项目

## 项目概述
本项目是一个专注于手机和电脑处理器性能排行的H5应用，旨在为用户提供直观、易用的处理器性能对比平台。应用支持手机处理器排行榜以及电脑处理器排行榜（包括CPU、GPU和内存组件），并针对移动设备进行了全面优化。

## 技术栈

### 前端
- **框架**：Vue3
- **构建工具**：Vite
- **语言**：TypeScript
- **路由**：Vue Router
- **HTTP客户端**：Axios

### 后端
- **框架**：Python FastAPI
- **服务器**：Uvicorn
- **数据处理**：自定义爬虫模块
- **数据存储**：JSON文件

## 核心功能

### 排行榜展示
- **手机处理器榜**：展示各类移动SoC的综合性能、CPU性能、GPU性能等指标
- **电脑处理器榜**：分为CPU、GPU和内存三个子模块，分别展示相应组件的性能排名

### 数据筛选与排序
- 支持按性能、功耗、发布年份等多种维度排序
- 提供品牌、年份、功耗等筛选条件
- 支持关键词搜索功能

### 数据更新机制
- 实现10分钟更新阈值逻辑，避免频繁抓取
- 提供手动更新按钮，用户可主动触发数据刷新
- 显示数据上次更新时间

## 项目结构

```
ProcessorRanking/
├── backend/              # 后端代码
│   ├── app/             # FastAPI应用主目录
│   │   ├── routers/     # API路由
│   │   ├── scrapers/    # 数据爬取模块
│   │   └── main.py      # 应用入口
│   ├── data/            # JSON数据存储目录
│   └── requirements.txt # Python依赖
└── frontend/            # 前端代码
    ├── src/             # 源代码目录
    │   ├── pages/       # 页面组件
    │   ├── components/  # 通用组件
    │   ├── services/    # API服务
    │   └── styles/      # 样式文件
    └── package.json     # NPM依赖
```

## API接口

- `GET /api/mobile-soc` - 获取手机处理器排行数据
- `GET /api/cpu` - 获取电脑CPU排行数据
- `GET /api/gpu` - 获取电脑GPU排行数据
- `GET /api/memory` - 获取内存排行数据
- `GET /api/meta` - 获取数据更新时间、来源、版本信息
- `POST /api/update` - 触发数据更新（受10分钟阈值限制）

## 数据字段规范

### 手机SoC
- id, name, brand, cpu_arch, gpu_arch, process_nm, release_year, score_cpu, score_gpu, score_total, tdp_w, efficiency

### CPU
- id, name, brand, cores, threads, base_clk, boost_clk, process_nm, tdp_w, release_year, score_single, score_multi, efficiency

### GPU
- id, name, brand, vram_gb, process_nm, tdp_w, release_year, score_3d, efficiency

### 内存
- id, name, type, freq_mhz, capacity_gb, timing, release_year, score_bandwidth

## 部署说明

### 后端部署
1. 安装Python依赖：`pip install -r backend/requirements.txt`
2. 启动FastAPI服务：`cd backend && python -m app.main`

### 前端部署
1. 安装NPM依赖：`cd frontend && npm install`
2. 开发模式：`npm run dev`
3. 生产构建：`npm run build`

## 注意事项
- 项目中的数据爬取模块遵守robots.txt规则和网站使用条款
- 数据更新机制设有10分钟阈值限制，避免频繁抓取
- 应用已针对移动端进行优化，支持375px、480px、768px、1024px等断点尺寸
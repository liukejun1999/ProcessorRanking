总体目标
- 前端：Vue3 H5，手机与平板等移动端适配；手机处理器榜与电脑处理器榜（CPU/GPU/内存）分开实现
- 后端：Python FastAPI 提供统一 API；爬取可信站点排行数据，规范化后保存为本地 JSON，供前端调用

后端架构
- 技术栈：Python 3.x、FastAPI、Uvicorn
- 目录：app/routers、app/services、app/scrapers、app/models、data/
- 数据文件：data/mobile-soc.json、data/pc-cpu.json、data/pc-gpu.json、data/pc-memory.json、data/meta.json

API 设计（示例）
- GET /api/mobile-soc?sort=score_total&order=desc&brand=&year_from=&year_to=&tdp_max=&q=
- GET /api/cpu?sort=score_multi&order=desc&brand=&cores_min=&tdp_max=&year_from=&q=
- GET /api/gpu?sort=score_3d&order=desc&brand=&vram_min=&tdp_max=&year_from=&q=
- GET /api/memory?sort=score_bandwidth&order=desc&type=&freq_min=&capacity_min=&year_from=&q=
- GET /api/meta 返回数据更新时间、来源、版本
- 响应统一：items、total、updated_at、source

数据规范与字段
- 手机 SoC：id、name、brand、cpu_arch、gpu_arch、process_nm、release_year、score_cpu、score_gpu、score_total、tdp_w、efficiency
- CPU：id、name、brand、cores、threads、base_clk、boost_clk、process_nm、tdp_w、release_year、score_single、score_multi、efficiency
- GPU：id、name、brand、vram_gb、process_nm、tdp_w、release_year、score_3d、efficiency
- Memory：id、name、type、freq_mhz、capacity_gb、timing、release_year、score_bandwidth
- 统一单位与命名，提供版本号与时间戳；去重与别名映射（如 i7-12700 vs 12700）

爬虫策略
- 站点选择：公开排行榜或基准网站；遵守 robots.txt 与使用条款
- 解析流程：fetch → parse → normalize → dedupe → score → save JSON
- 异常处理：网络失败重试、结构变化告警、字段缺失回退
- 速率控制：限速、随机 UA、请求间隔；必要时使用缓存与离线更新
- 更新机制：APScheduler 定时任务（每日/每周）；失败回退至上次稳定版本

JSON 落盘与校验
- 保存到 data/*.json；写入临时文件后原子替换，避免部分写入
- 校验：schema 校验、条目数量与关键字段完整性
- meta.json 记录更新时间、来源统计与版本号

FastAPI 实现要点
- 路由：/api/*
- 过滤与排序：服务端支持；分页或前端一次性加载视数据量而定
- CORS：允许前端域访问；Cache-Control 与 ETag/Last-Modified 支持
- 性能：gzip 压缩、轻量中间件；必要时启用文件静态服务

前端集成（Vue3）
- 路由：/mobile-processors 与 /pc-processors（Tabs：CPU/GPU/内存）
- 数据加载：Axios 请求上述 API；防抖搜索、切换排序/筛选参数映射
- 表格/卡片：在小屏展示关键列，次要信息折叠；支持对比（最多 3 项）
- 移动适配：viewport、流式布局、断点（375/480/768/1024）、触控优化
- 性能：虚拟列表（大数据量）、路由懒加载、结果缓存

质量与测试
- 后端：解析单测、契约测试（pydantic schema）、端到端抓取回归
- 前端：交互逻辑测试（排序/筛选/对比）、兼容性手动验收
- 安全与合规：尊重站点条款、最小抓取频率、清晰来源标注

里程碑
1) FastAPI 初始化、数据 schema 与 API 草案
2) 选定数据源，完成手机 SoC 爬虫与 JSON；实现 /api/mobile-soc
3) 完成 CPU/GPU/内存爬虫与 JSON；实现对应 API
4) 前端页面 MVP：手机榜、电脑榜 Tabs；排序/筛选/搜索联通后端
5) 对比功能、虚拟列表与缓存；可访问性完善
6) 测试、优化与交付

请确认该计划与后端选型。如果同意，我将按里程碑推进，并优先落地后端数据管线与 API，随后实现前端页面与交互。
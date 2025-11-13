<template>
  <div class="page">
    <!-- 顶部导航栏 -->
    <header class="header">
      <h1 class="title">电脑{{ tab === 'cpu' ? 'CPU' : tab === 'gpu' ? 'GPU' : '内存' }}天梯榜</h1>
    </header>
    
    <!-- 搜索框和类型选择 -->
    <div class="search-container">
      <div class="search-wrapper">
        <input class="search-input" v-model="q" placeholder="搜索" @input="onSearch" />
        <select class="type-select" v-model="tab" @change="onTabChange">
          <option value="cpu">CPU</option>
          <option value="gpu">GPU</option>
        </select>
      </div>
    </div>
    
    <!-- 卡片列表 -->
    <div class="grid">
      <div v-if="loading" class="loading">加载中</div>
      <div v-else-if="items.length===0" class="no-data">暂无数据</div>
      <div v-else class="cards-container">
        <div v-for="(item, index) in items" :key="item.id" class="card-item">
          <div class="rank-badge">{{ index + 1 }}</div>
          <div class="card-content">
            <img :src="`/src/assets/logo/${(item.brand || 'default').toLowerCase()}.png`" :alt="item.brand || '未知'" class="brand-logo" @error="handleImageError($event, item)" />
            <div class="info">
              <div class="name">{{ item.name }}</div>
              <div class="score">
                <span>评分: {{ valueKey(item) || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { getCpu, getGpu, getMeta, postUpdate } from '../services/api'

const tab = ref<'cpu'|'gpu'>('cpu')
const items = ref<any[]>([])
const lastUpdatedText = ref('未知')
const loading = ref(false)
const q = ref('')
const sort = ref('score_multi')
const order = ref('desc')
let timer: any

watch(tab, () => {
  if (tab.value === 'cpu') sort.value = 'score_multi'
  if (tab.value === 'gpu') sort.value = 'score_3d'
  refreshMeta()
  fetchData()
})

async function refreshMeta(){
  const m = await getMeta()
  const ts = m.updated_at
  lastUpdatedText.value = ts ? ts : '未知'
}

function onSearch(){
  clearTimeout(timer)
  timer = setTimeout(fetchData, 300)
}

function onTabChange() {
  if (tab.value === 'cpu') sort.value = 'score_multi'
  else if (tab.value === 'gpu') sort.value = 'score_3d'
  else sort.value = 'score_bandwidth'
  refreshMeta()
  fetchData()
}

function valueKey(item: any){
  if (tab.value === 'cpu') return item.score_multi
  if (tab.value === 'gpu') return item.score_3d
  return item.score_bandwidth
}

function handleImageError(event: Event, item: any) {
  const target = event.target as HTMLImageElement;
  target.src = `/src/assets/logo/default.png`;
}

async function fetchData(){
  loading.value = true
  let r
  if (tab.value === 'cpu') r = await getCpu({ q: q.value, sort: sort.value, order: order.value })
  else if (tab.value === 'gpu') r = await getGpu({ q: q.value, sort: sort.value, order: order.value })
  items.value = r.items
  loading.value = false
}

refreshMeta()
fetchData()
</script>

<style scoped>
.page {
  min-height: calc(100vh - 60px);
  transition: background-color 0.3s ease;
}

/* 默认浅色主题样式 */
.header {
  background: linear-gradient(135deg, #00c6ff, #0072ff);
  padding: 16px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 10px rgba(0, 114, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
  animation: techShine 3s infinite;
}

@keyframes techShine {
  0% { transform: rotate(0deg) translateX(-100%); }
  100% { transform: rotate(0deg) translateX(100%); }
}

.title {
  color: #ffffff;
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

.search-container {
  padding: 12px 0;
  background-color: #f8f9fa;
}

.grid {
  padding: 0;
  margin-top: 12px;
}

.search-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  color: #333;
  font-size: 16px;
  outline: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 3px rgba(0, 114, 255, 0.1);
}

.type-select {
  padding: 12px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #ffffff;
  color: #333;
  font-size: 14px;
  outline: none;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.type-select:hover {
  border-color: #0072ff;
}

.type-select:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 3px rgba(0, 114, 255, 0.1);
}

/* 深色主题适配 */
:global(.theme-light) .page {
  background-color: #ffffff;
}

:global(.theme-light) .card-item {
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-color: #e0e0e0;
}

:global(.theme-light) .name {
  color: #333;
}

:global(.theme-light) .score {
  color: #666;
}

:global(.theme-light) .brand-logo {
  background-color: #f0f0f0;
}

/* 深色主题样式 */
:global(html:not(.theme-light)) .header {
  background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
  border-bottom-color: #444;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

:global(html:not(.theme-light)) .header::before {
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
}

:global(html:not(.theme-light)) .title {
  color: #ffffff;
}

:global(html:not(.theme-light)) .search-container {
  background-color: #1a1a1a;
  border-bottom-color: #444;
}

:global(html:not(.theme-light)) .card-item {
  background: linear-gradient(135deg, #2a2a2a, #1a1a1a);
  border-color: #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:global(html:not(.theme-light)) .card-item:hover {
  box-shadow: 0 4px 12px rgba(0, 198, 255, 0.1);
}

:global(html:not(.theme-light)) .name {
  color: #fff;
}

:global(html:not(.theme-light)) .score {
  color: #ccc;
}

:global(html:not(.theme-light)) .brand-logo {
  background-color: #333;
}

:global(html:not(.theme-light)) .search-input {
  background-color: #2a2a2a;
  color: #fff;
  border-color: #444;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

:global(html:not(.theme-light)) .search-input:focus {
  border-color: #00c6ff;
  box-shadow: 0 0 0 3px rgba(0, 198, 255, 0.2);
}

:global(html:not(.theme-light)) .type-select {
  background-color: #2a2a2a;
  color: #fff;
  border-color: #444;
  background-image: linear-gradient(45deg, transparent 50%, #00c6ff 50%);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

:global(html:not(.theme-light)) .type-select:hover {
  border-color: #00c6ff;
}

:global(html:not(.theme-light)) .type-select:focus {
  border-color: #00c6ff;
  box-shadow: 0 0 0 3px rgba(0, 198, 255, 0.2);
}

/* 卡片容器样式 */
.cards-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

/* 单个卡片样式 */
.card-item {
  position: relative;
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.card-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 114, 255, 0.1);
}

/* 排名徽章 */
.rank-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #0072ff, #00c6ff);
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

/* 卡片内容布局 */
.card-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 品牌logo样式 */
.brand-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
  border-radius: 8px;
  background-color: #f0f0f0;
  padding: 8px;
}

/* 信息区域样式 */
.info {
  flex: 1;
}

/* 处理器名称样式 */
.name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

/* 分数显示样式 */
.score {
  display: flex;
  gap: 24px;
  font-size: 16px;
  color: #666;
}

.score span {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 加载和无数据状态 */
.loading, .no-data {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}


</style>
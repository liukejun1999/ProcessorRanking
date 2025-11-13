<template>
  <div class="page">
    <!-- 顶部导航栏 -->
    <header class="header">
      <h1 class="title">我的</h1>
    </header>
    
    <div class="settings-container">
      <!-- 主题切换设置 -->
      <div class="setting-item">
        <div class="setting-label">主题切换</div>
        <div class="setting-control">
          <select v-model="currentTheme" @change="changeTheme" class="theme-select">
            <option value="dark">深色主题</option>
            <option value="light">浅色主题</option>
          </select>
        </div>
      </div>
      
      <!-- 更新排行榜设置 -->
      <div class="setting-item">
        <div class="setting-label">更新排行榜</div>
        <div class="setting-control">
          <select v-model="updateType" class="update-select">
            <option value="all">全部更新</option>
            <option value="mobile-soc">手机SOC</option>
            <option value="pc-cpu">电脑CPU</option>
            <option value="pc-gpu">电脑GPU</option>
            <option value="pc-memory">电脑内存</option>
          </select>
          <button class="update-btn" @click="updateRanking" :disabled="isUpdating">
            {{ isUpdating ? '更新中...' : '立即更新' }}
          </button>
        </div>
      </div>
      
      <!-- 更新时间信息 -->
      <div class="update-info" v-if="lastUpdatedText">
        <p>上次更新时间：{{ lastUpdatedText }}</p>
        <p class="update-hint" v-if="!canUpdate">* 距离上次更新不足10分钟，请稍后再试</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMeta, postUpdate } from '../services/api'

const currentTheme = ref<'dark'|'light'>('light')
const updateType = ref<'all'|'mobile-soc'|'pc-cpu'|'pc-gpu'|'pc-memory'>('all')
const lastUpdatedText = ref('')
const isUpdating = ref(false)
const canUpdate = ref(true)

// 主题切换函数
function changeTheme() {
  const el = document.documentElement
  if (currentTheme.value === 'light') {
    el.classList.add('theme-light')
  } else {
    el.classList.remove('theme-light')
  }
  try {
    localStorage.setItem('theme', currentTheme.value)
  } catch (e) {
    console.error('Failed to save theme to localStorage:', e)
  }
}

// 刷新更新时间信息
async function refreshMeta() {
  const m = await getMeta()
  const ts = m.updated_at
  lastUpdatedText.value = ts ? ts : '未知'
  
  // 检查是否可以更新（10分钟限制）
  if (ts) {
    try {
      const last = new Date(ts)
      const now = new Date()
      const delta = (now.getTime() - last.getTime()) / 1000
      canUpdate.value = delta >= 600
    } catch {
      canUpdate.value = true
    }
  } else {
    canUpdate.value = true
  }
}

// 更新排行榜
async function updateRanking() {
  if (!canUpdate.value || isUpdating.value) return
  
  isUpdating.value = true
  try {
    await postUpdate(updateType.value)
    await refreshMeta()
  } catch (error) {
    console.error('Update failed:', error)
    alert('更新失败，请稍后重试')
  } finally {
    isUpdating.value = false
  }
}

// 初始化
onMounted(() => {
  // 加载保存的主题设置
  try {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'light' || savedTheme === 'dark') {
      currentTheme.value = savedTheme as 'dark' | 'light'
    } else {
      // 默认使用浅色主题
      currentTheme.value = 'light'
    }
  } catch {
    // 如果无法读取localStorage，使用默认值
  }
  
  // 应用当前主题
  changeTheme()
  
  // 刷新更新时间
  refreshMeta()
})
</script>

<style scoped>
.page {
  min-height: calc(100vh - 60px);
}

.header {
  background: linear-gradient(135deg, #0072ff, #00c6ff);
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

.settings-container {
  padding: 12px 0;
}

/* 默认浅色主题样式 */
.setting-item {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.setting-item:hover {
  box-shadow: 0 4px 12px rgba(0, 114, 255, 0.1);
}

.setting-label {
  color: #333;
  font-size: 16px;
  margin-bottom: 12px;
  font-weight: 500;
}

.setting-control {
  display: flex;
  gap: 12px;
  align-items: center;
}

.theme-select,
.update-select {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  color: #333;
  font-size: 16px;
  outline: none;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.theme-select:hover,
.update-select:hover {
  border-color: #0072ff;
}

.theme-select:focus,
.update-select:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 3px rgba(0, 114, 255, 0.1);
}

.update-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #0072ff, #00c6ff);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 114, 255, 0.3);
}

.update-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 114, 255, 0.4);
}

.update-btn:disabled {
  background: linear-gradient(135deg, #666, #999);
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.update-info {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e0e0e0;
  color: #666;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.update-info p {
  margin: 8px 0;
  font-size: 14px;
}

.update-hint {
  color: #ff9800 !important;
  font-size: 12px !important;
}

/* 浅色主题样式 */
:global(.theme-light) .header {
  background-color: #f5f5f5;
  border-bottom-color: #ddd;
}

:global(.theme-light) .title,
:global(.theme-light) .setting-label {
  color: #333;
}

:global(.theme-light) .setting-item,
:global(.theme-light) .update-info {
  background-color: #f5f5f5;
  border-color: #ddd;
  color: #333;
}

:global(.theme-light) .theme-select,
:global(.theme-light) .update-select {
  background-color: #fff;
  border-color: #ddd;
  color: #333;
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

:global(html:not(.theme-light)) .setting-item {
  background-color: #1a1a1a;
  border-color: #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:global(html:not(.theme-light)) .setting-item:hover {
  box-shadow: 0 4px 12px rgba(0, 198, 255, 0.2);
}

:global(html:not(.theme-light)) .setting-label {
  color: #fff;
}

:global(html:not(.theme-light)) .theme-select,
:global(html:not(.theme-light)) .update-select {
  background-color: #2a2a2a;
  color: #fff;
  border-color: #444;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  background-image: linear-gradient(45deg, transparent 50%, #00c6ff 50%);
}

:global(html:not(.theme-light)) .theme-select:hover,
:global(html:not(.theme-light)) .update-select:hover {
  border-color: #00c6ff;
}

:global(html:not(.theme-light)) .theme-select:focus,
:global(html:not(.theme-light)) .update-select:focus {
  border-color: #00c6ff;
  box-shadow: 0 0 0 3px rgba(0, 198, 255, 0.2);
}

:global(html:not(.theme-light)) .update-btn {
  background: linear-gradient(135deg, #00c6ff, #0072ff);
  box-shadow: 0 2px 8px rgba(0, 198, 255, 0.3);
}

:global(html:not(.theme-light)) .update-btn:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(0, 198, 255, 0.4);
}

:global(html:not(.theme-light)) .update-info {
  background-color: #1a1a1a;
  border-color: #444;
  color: #ccc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>
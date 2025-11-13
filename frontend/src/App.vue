<template>
  <div class="container">
    <main class="main-content">
      <router-view />
    </main>
    <nav class="bottom-nav">
      <router-link class="nav-item" to="/mobile-processors">
        <span class="nav-icon">📱</span>
        <span class="nav-text">手机</span>
      </router-link>
      <router-link class="nav-item" to="/pc-processors">
        <span class="nav-icon">💻</span>
        <span class="nav-text">电脑</span>
      </router-link>
      <router-link class="nav-item" to="/my-settings">
        <span class="nav-icon">⚙️</span>
        <span class="nav-text">我的</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const theme = ref<'dark'|'light'>('light')

function applyTheme(t: 'dark'|'light'){
  theme.value = t
  const el = document.documentElement
  if (t === 'light') el.classList.add('theme-light')
  else el.classList.remove('theme-light')
  try { localStorage.setItem('theme', t) } catch {}
}

function toggleTheme(){
  applyTheme(theme.value === 'dark' ? 'light' : 'dark')
}

onMounted(() => {
  let t: 'dark'|'light' = 'light'
  try {
    const s = localStorage.getItem('theme')
    if (s === 'light' || s === 'dark') t = s as any
  } catch {}
  applyTheme(t)
})
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding-bottom: 60px;
  transition: background-color 0.3s ease;
}

.main-content {
  flex: 1;
  padding: 16px;
}

/* 默认浅色主题样式 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-top: 1px solid #e0e0e0;
  padding: 8px 0;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 114, 255, 0.05);
  backdrop-filter: blur(10px);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #666;
  text-decoration: none;
  padding: 8px 0;
  min-width: 30%;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item:hover {
  background-color: rgba(0, 114, 255, 0.05);
}

.nav-item.router-link-active {
  color: #0072ff;
  background-color: rgba(0, 114, 255, 0.08);
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  border-radius: 3px;
}

.nav-icon {
  font-size: 24px;
  margin-bottom: 4px;
  transition: transform 0.3s ease;
}

.nav-item.router-link-active .nav-icon {
  transform: scale(1.1);
}

.nav-text {
  font-size: 12px;
  font-weight: 500;
}

/* 深色主题适配 */
:global(.theme-light) .container {
  background-color: #ffffff;
}

:global(.theme-light) .bottom-nav {
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-top-color: #e0e0e0;
  box-shadow: 0 -2px 10px rgba(0, 114, 255, 0.05);
}

/* 深色主题样式 */
:global(html:not(.theme-light)) .container {
  background-color: #242424;
}

:global(html:not(.theme-light)) .bottom-nav {
  background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
  border-top-color: #444;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
}

:global(html:not(.theme-light)) .nav-item {
  color: #ccc;
}

:global(html:not(.theme-light)) .nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

:global(html:not(.theme-light)) .nav-item.router-link-active {
  color: #00c6ff;
  background-color: rgba(0, 198, 255, 0.1);
}

:global(html:not(.theme-light)) .nav-item.router-link-active::after {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
}
</style>
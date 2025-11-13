import { createRouter, createWebHistory } from 'vue-router'
import MobileProcessors from '../pages/MobileProcessors.vue'
import PcProcessors from '../pages/PcProcessors.vue'
import MySettings from '../pages/MySettings.vue'

const routes = [
  { path: '/', redirect: '/mobile-processors' },
  { path: '/mobile-processors', component: MobileProcessors },
  { path: '/pc-processors', component: PcProcessors },
  { path: '/my-settings', component: MySettings }
] as const

export default createRouter({
  history: createWebHistory(),
  routes
})
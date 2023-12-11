import { createRouter, createWebHistory } from 'vue-router'
import LeaderBoardView from '@/views/LeaderBoardView';


const routes = [

  {
    path: '/',
    name: 'leader',
    component: LeaderBoardView
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

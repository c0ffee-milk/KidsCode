<template>
  <div class="pass-page">
    <h1>🎉 恭喜通过第{{ $route.params.levelId }}关！</h1>
    <p>你太棒了，继续挑战下一关吧！</p>
    <router-link :to="nextLevelUrl">
      <button class="next-btn">下一关</button>
    </router-link>
    <router-link to="/">
      <button class="home-btn">返回首页</button>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const levelId = Number(route.params.levelId)
const nextLevelId = levelId + 1
const nextLevelUrl = computed(() => `/level/${nextLevelId}`)
</script>

<style scoped>
.pass-page {
  text-align: center;
  padding: 60px 0;
}
.pass-page h1 {
  font-size: 2.4rem;
  color: #f1b500;
  margin-bottom: 20px;
}
.pass-page p {
  margin-bottom: 40px;
  color: #666;
}
.next-btn, .home-btn {
  margin: 8px 12px;
  padding: 12px 36px;
  font-size: 1.1rem;
  border-radius: 24px;
  border: none;
  background: linear-gradient(90deg, #ffe97a, #ffb84c);
  color: #222;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 16px #ffb84c33;
  transition: background 0.2s;
}
.next-btn:hover, .home-btn:hover {
  background: linear-gradient(90deg, #ffb84c, #ffe97a);
}
</style>

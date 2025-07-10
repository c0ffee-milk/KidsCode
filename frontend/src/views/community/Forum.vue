<template>
  <!-- 论坛主页面容器 -->
  <div class="forum-page">
    <!-- 内容居中容器 -->
    <div class="forum-container">
      <!-- 标题和简介 -->
      <div class="section-header">
        <h2>讨论论坛</h2>
        <p>在这里你可以提问、交流和分享少儿编程学习的点滴</p>
      </div>
      <!-- 输入框和发布按钮 -->
      <div class="forum-actions">
        <el-input
          v-model="newTopicTitle"
          placeholder="输入问题或话题，按回车发布"
          class="forum-input"
          size="large"
          @keyup.enter.native="addTopic"
          clearable
        >
          <!-- 输入框后缀按钮 -->
          <template #append>
            <el-button
              type="primary"
              @click="addTopic"
              :disabled="!newTopicTitle.trim()"
            >发布</el-button>
          </template>
        </el-input>
      </div>
      <!-- 话题列表 -->
      <div class="forum-list" v-if="topics.length">
        <!-- 单个话题，可点击 -->
        <div
          class="forum-topic"
          v-for="(topic, index) in topics"
          :key="topic.id"
          @click="selectTopic(index)"
          :class="{ active: selectedTopicIndex === index }"
        >
          <span class="topic-title">{{ topic.title }}</span>
          <span class="topic-meta">{{ topic.comments.length }} 回复</span>
        </div>
      </div>
      <!-- 无话题提示 -->
      <div v-else class="forum-empty">暂无话题，快来发布吧！</div>

      <!-- 右侧抽屉，显示话题详情和回复 -->
      <el-drawer
        v-model="drawerVisible"
        :with-header="false"
        size="420px"
        custom-class="forum-drawer"
      >
        <!-- 抽屉内容 -->
        <div v-if="selectedTopic" class="forum-detail">
          <div class="detail-header">
            <!-- 话题标题 -->
            <h3>{{ selectedTopic.title }}</h3>
            <!-- 关闭按钮 -->
            <el-button
              icon="el-icon-close"
              circle
              size="small"
              @click="closeDetail"
              class="close-btn"
            />
          </div>
          <!-- 评论列表 -->
          <div class="comments-list" v-if="selectedTopic.comments.length">
            <div
              class="comment"
              v-for="(comment, idx) in selectedTopic.comments"
              :key="idx"
            >
              <span class="comment-user">{{ comment.user }}</span>
              <span class="comment-text">{{ comment.text }}</span>
              <span class="comment-time">{{ comment.time }}</span>
            </div>
          </div>
          <!-- 无回复提示 -->
          <div v-else class="forum-empty">暂时还没有回复，快来抢沙发吧！</div>
          <!-- 回复输入框和按钮 -->
          <div class="add-comment">
            <el-input
              v-model="newComment"
              placeholder="输入你的回复"
              class="forum-input"
              size="large"
              @keyup.enter.native="addComment"
              clearable
            >
              <template #append>
                <el-button
                  type="primary"
                  @click="addComment"
                  :disabled="!newComment.trim()"
                >回复</el-button>
              </template>
            </el-input>
          </div>
        </div>
      </el-drawer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElInput, ElButton, ElDrawer } from 'element-plus';

// 话题示例
const topics = ref([
  {
    id: 1,
    title: '如何用Scratch制作动画？',
    comments: [
      {
        user: '小明',
        text: '可以先画角色，再用积木让角色动起来！',
        time: '2025-07-10 15:15'
      }
    ]
  },
  {
    id: 2,
    title: '编程遇到问题怎么办？',
    comments: [
      {
        user: '小红',
        text: '可以在这里提问，大家一起帮忙。',
        time: '2025-07-10 15:20'
      }
    ]
  }
]);
// 新话题标题输入
const newTopicTitle = ref('');
// 当前选中话题的索引
const selectedTopicIndex = ref<number|null>(null);
// 新回复输入
const newComment = ref('');
// 控制抽屉显示
const drawerVisible = ref(false);

// 当前选中话题
const selectedTopic = computed(() => {
  if (
    selectedTopicIndex.value !== null &&
    topics.value[selectedTopicIndex.value]
  ) {
    return topics.value[selectedTopicIndex.value];
  }
  return null;
});

// 添加新话题
function addTopic() {
  const title = newTopicTitle.value.trim();
  if (title) {
    topics.value.unshift({
      id: Date.now(),
      title,
      comments: []
    });
    newTopicTitle.value = '';
  }
}

// 选中话题，弹出抽屉
function selectTopic(index: number) {
  selectedTopicIndex.value = index;
  drawerVisible.value = true;
  newComment.value = '';
}
// 添加新回复
function addComment() {
  const commentText = newComment.value.trim();
  if (commentText && selectedTopicIndex.value !== null) {
    topics.value[selectedTopicIndex.value].comments.push({
      user: '小朋友',  // 默认用户名
      text: commentText,
      time: new Date().toLocaleString('zh-CN', { hour12: false }) // 当前时间
    });
    newComment.value = '';
  }
}
// 关闭抽屉，清空数据
function closeDetail() {
  drawerVisible.value = false;
  setTimeout(() => {
    selectedTopicIndex.value = null;
    newComment.value = '';
  }, 300);
}
</script>

<style scoped>
/* 整体页面背景和间距 */
.forum-page {
  width: 100%;
  min-height: calc(100vh - 144px);
  background: linear-gradient(135deg, rgba(255,255,255,0.94) 0%, rgba(248,250,252,0.98) 100%);
  padding: 80px 0;
}
/* 内容居中和卡片效果 */
.forum-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 0 24px 60px 24px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.06);
}
/* 标题和说明居中 */
.section-header {
  text-align: center;
  margin-bottom: 48px;
}
.section-header h2 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 12px;
  letter-spacing: 1px;
}
.section-header p {
  font-size: 1.08rem;
  color: #64748b;
  margin: 0 auto;
  line-height: 1.6;
}

/* 发帖输入框区域 */
.forum-actions {
  margin-bottom: 28px;
}
.forum-input :deep(.el-input__inner) {
  border-radius: 14px;
  font-size: 1em;
  padding: 14px 16px;
}
.forum-input :deep(.el-input-group__append),
.add-comment .forum-input :deep(.el-input-group__append) {
  border-radius: 0 14px 14px 0 !important;
}

/* 话题列表间距 */
.forum-list {
  margin-bottom: 32px;
}
/* 单个话题卡片风格 */
.forum-topic {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border-radius: 16px;
  padding: 18px 22px;
  margin-bottom: 16px;
  cursor: pointer;
  font-size: 1.13em;
  border: 1.5px solid transparent;
  transition: background 0.18s, border-color 0.2s;
  box-shadow: 0 2px 12px rgba(102,126,234,0.03);
}
/* 选中/悬停高亮 */
.forum-topic.active,
.forum-topic:hover {
  background: #e3eafe;
  border-color: #a5b4fc;
}
.topic-title {
  font-weight: 600;
  color: #3b3b7b;
}
.topic-meta {
  font-size: 0.96em;
  color: #64748b;
  margin-left: 10px;
}
/* 无内容提示 */
.forum-empty {
  text-align: center;
  color: #bdbdbd;
  margin: 32px 0;
  font-size: 1.09em;
}

/* 抽屉样式 */
.forum-drawer {
  border-radius: 22px 0 0 22px;
  box-shadow: -2px 0 18px rgba(102, 126, 234, 0.06);
}
/* 详情内容 */
.forum-detail {
  padding: 10px 0 0 0;
}
/* 标题和关闭按钮 */
.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.detail-header h3 {
  color: #4f46e5;
  font-size: 1.18em;
  font-weight: 700;
  margin: 0;
  padding: 0;
}
/* 关闭按钮样式 */
.close-btn {
  background: #f8fafc !important;
  color: #64748b !important;
  box-shadow: none !important;
}
/* 评论列表样式 */
.comments-list {
  margin-bottom: 18px;
}
.comment {
  margin-bottom: 12px;
  padding: 10px 12px;
  background: #f1f5fa;
  border-radius: 12px;
  font-size: 1em;
  border-left: 4px solid #a5b4fc;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.comment-user {
  color: #667eea;
  font-weight: 600;
}
.comment-text {
  color: #374151;
}
.comment-time {
  color: #bdbdbd;
  font-size: 0.9em;
  align-self: flex-end;
}
/* 回复输入框区域 */
.add-comment {
  margin-top: 24px;
}
.add-comment .forum-input {
  width: 100%;
}
/* 移动端自适应 */
@media (max-width: 768px) {
  .forum-container {
    padding: 0 10px 40px 10px;
    max-width: 99vw;
  }
  .forum-topic {
    padding: 13px 12px;
    font-size: 1em;
  }
  .forum-drawer {
    width: 100vw !important;
    border-radius: 0;
  }
}
</style>

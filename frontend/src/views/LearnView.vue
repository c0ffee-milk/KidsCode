<template>
  <div class="learn-page">
    <div class="learn-container">
      <div class="learn-header">
        <h1 class="page-title">编程闯关学习</h1>
        <p class="page-desc">通过互动式编程练习，掌握编程基础知识</p>
      </div>
      
      <div class="learn-content">
        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <span>学习进度</span>
              <el-tag type="primary">第 {{ currentStep + 1 }} 关</el-tag>
            </div>
          </template>
          <el-steps :active="currentStep" finish-status="success" align-center class="learn-steps">
            <el-step v-for="(step, idx) in steps" :key="idx" :title="step.title" />
          </el-steps>
        </el-card>
        
        <div class="learn-body">
          <div class="left-panel">
            <el-card class="task-card">
              <template #header>
                <div class="card-header">
                  <el-icon><Document /></el-icon>
                  <span>编程任务</span>
                </div>
              </template>
              <div class="task-content">
                <el-alert
                  :title="steps[currentStep].desc"
                  type="info"
                  show-icon
                  :closable="false"
                />
                <div class="task-tips">
                  <h4>💡 小提示：</h4>
                  <ul>
                    <li>仔细阅读任务要求</li>
                    <li>可以参考右侧的代码示例</li>
                    <li>运行代码查看结果</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-card class="result-card" v-if="result">
              <template #header>
                <div class="card-header">
                  <el-icon><Monitor /></el-icon>
                  <span>运行结果</span>
                </div>
              </template>
              <div class="result-content">
                <pre class="result-text">{{ result }}</pre>
              </div>
            </el-card>
          </div>
          
          <div class="right-panel">
            <el-card class="editor-card">
              <template #header>
                <div class="card-header">
                  <el-icon><Edit /></el-icon>
                  <span>代码编辑器</span>
                </div>
              </template>
              <div class="editor-content">
                <el-input
                  v-model="code"
                  type="textarea"
                  :rows="12"
                  placeholder="在这里写代码..."
                  show-word-limit
                  maxlength="2000"
                  class="code-editor"
                />
                <div class="editor-actions">
                  <el-button type="primary" size="large" @click="runCode" :loading="isRunning">
                    <el-icon><CaretRight /></el-icon>
                    运行代码
                  </el-button>
                  <el-button size="large" @click="resetCode">
                    <el-icon><RefreshRight /></el-icon>
                    重置代码
                  </el-button>
                  <el-button type="success" size="large" @click="nextStep" :disabled="currentStep >= steps.length - 1">
                    <el-icon><Right /></el-icon>
                    下一关
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const steps = ref([
  { 
    title: '认识变量', 
    desc: '请声明一个变量 message，赋值为 "Hello, World!"，然后使用 console.log() 输出这个变量',
    code: 'let message = "Hello, World!";\nconsole.log(message);'
  },
  { 
    title: '循环与条件', 
    desc: '使用 for 循环输出数字 1 到 5，每个数字前加上 "数字: " 的前缀',
    code: 'for(let i = 1; i <= 5; i++) {\n  console.log("数字: " + i);\n}'
  },
  { 
    title: '函数与模块', 
    desc: '编写一个名为 greet 的函数，接收一个 name 参数，返回 "你好, {name}!" 的问候语，然后调用这个函数',
    code: 'function greet(name) {\n  return "你好, " + name + "!";\n}\nconsole.log(greet("小朋友"));'
  }
])

const currentStep = ref(0)
const code = ref(steps.value[0].code)
const result = ref('')
const isRunning = ref(false)

function runCode() {
  if (!code.value.trim()) {
    ElMessage.warning('请输入代码')
    return
  }
  
  isRunning.value = true
  result.value = ''
  
  setTimeout(() => {
    try {
      const logs: string[] = []
      const mockConsole = {
        log: (...args: any[]) => {
          logs.push(args.map(arg => String(arg)).join(' '))
        }
      }
      
      const func = new Function('console', code.value)
      func(mockConsole)
      
      result.value = logs.length > 0 ? logs.join('\n') : '代码执行完成，没有输出'
      ElMessage.success('代码运行成功！')
    } catch (error) {
      result.value = `❌ 错误: ${error instanceof Error ? error.message : '代码执行失败'}`
      ElMessage.error('代码有误，请检查语法！')
    } finally {
      isRunning.value = false
    }
  }, 800)
}

function resetCode() {
  code.value = steps.value[currentStep.value].code
  result.value = ''
  ElMessage.info('代码已重置为初始状态')
}

function nextStep() {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
    code.value = steps.value[currentStep.value].code
    result.value = ''
    ElMessage.success(`🎉 恭喜进入第 ${currentStep.value + 1} 关！`)
  } else {
    ElMessage.success('🎊 恭喜完成所有关卡！')
  }
}
</script>

<style scoped>
.learn-page {
  min-height: calc(100vh - 160px);
  padding: 32px 0;
}

.learn-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.learn-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}

.page-desc {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.learn-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.progress-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  font-size: 1.1rem;
}

.card-header .el-icon {
  margin-right: 8px;
}

.learn-steps {
  padding: 20px 0;
}

.learn-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.task-card,
.result-card,
.editor-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.task-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.task-tips {
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.task-tips h4 {
  margin-bottom: 8px;
  color: #334155;
}

.task-tips ul {
  margin-left: 20px;
  color: #64748b;
}

.task-tips li {
  margin-bottom: 4px;
  line-height: 1.5;
}

.editor-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.code-editor {
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
}

.editor-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.result-content {
  max-height: 300px;
  overflow-y: auto;
}

.result-text {
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 8px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .learn-body {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .learn-container {
    padding: 0 16px;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .editor-actions {
    flex-direction: column;
  }
  
  .editor-actions .el-button {
    width: 100%;
  }
}
</style>
# Github合作指南

## 1. 克隆远程仓库

远程仓库有两个branch：main和dev，我们在dev分支上进行开发

```shell
git clone --branch dev git@github.com:c0ffee-milk/KidsCode.git
```

## 2. 代码同步

1. 在开始coding前建议先pull远程仓库同步代码

```shell
git pull
```

2. coding结束后提交代码，同步到远程仓库（建议开发完一个模块或功能就同步一次代码，不要积攒太多代码一次性同步）

```shell
git add .

git commit -m "info" # 在双引号内说明内容

git pull

git push
```

记得在push前一定先pull，pull之后如果有冲突请自行解决，一定不要强行push！！！

## 3. Conventional Commits规范

1. 完整规范参考: https://www.conventionalcommits.org

2. 常用类型(type):
- feat: 新功能
- fix: bug修复
- docs: 文档变更
- style: 代码格式调整
- refactor: 重构代码
- test: 测试相关
- chore: 构建/工具变更

示例：
- feat: 添加用户登录功能
- fix(router): 修复路由跳转问题
- docs: 更新API接口文档
- style: 调整代码格式
- refactor: 重构代码
- test: 添加用户登录测试用例
- chore: 更新依赖



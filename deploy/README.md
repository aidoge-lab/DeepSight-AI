# 🚀 部署脚本

这个目录包含了将 AI Insights Charts 部署到 GitHub Pages 的自动化脚本。

## 📁 文件说明

### `deploy-pages.sh` - 完整功能部署脚本

**功能特点：**
- 🔍 检查项目目录和 git 状态
- 🎨 彩色输出，用户体验更好
- ⚠️ 提醒用户提交未保存的更改
- 🔄 自动管理远程仓库配置
- 🧹 自动清理临时分支
- 📊 显示详细的部署信息
- 🌐 可选择自动打开网站

### `quick-deploy.sh` - 快速部署脚本

**功能特点：**
- ⚡ 极简设计，适用于频繁更新
- 🚀 一键快速部署
- 🧹 自动清理临时文件

## 🎯 使用方法

在项目根目录执行以下命令：

### 完整部署（推荐首次使用）
```bash
./deploy/deploy-pages.sh
```

### 快速部署（日常更新）
```bash
./deploy/quick-deploy.sh
```

## 📋 部署流程

1. **修改内容** - 更新 `insights/` 目录中的文件
2. **提交更改** - `git add . && git commit -m "更新内容"`
3. **执行部署** - 运行上述脚本之一
4. **访问网站** - 几分钟后访问 https://aidoge-lab.github.io/

## ⚠️ 注意事项

- 脚本需要在项目根目录执行
- 确保有推送到 GitHub 的权限
- 首次使用会自动配置远程仓库
- 部署完成后，GitHub Pages 可能需要几分钟来更新

## 🔧 自定义配置

如需修改目标仓库或其他配置，请编辑 `deploy-pages.sh` 中的配置部分：

```bash
PAGES_REPO="https://github.com/aidoge-lab/aidoge-lab.github.io.git"
SOURCE_DIR="insights"
REMOTE_NAME="pages"
``` 
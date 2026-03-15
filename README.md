# image-gen

AI 图像生成 Skill，基于 Gemini Flash Image 模型，支持文生图、图+文生图、多比例、多分辨率。

## 安装

### OpenClaw

```bash
# ClawHub 安装（推荐）
clawhub install ai-image-gen

# Git 直接安装
cd /path/to/your/workspace/skills
git clone git@github.com:qiujiahong/image-gen.git ai-image-gen
```

### Claude Code

```bash
# 克隆到 Claude Code 的 skills 目录
cd ~/.claude/skills
git clone git@github.com:qiujiahong/image-gen.git ai-image-gen
```

### OpenCode

```bash
# 克隆到 OpenCode 的 skills 目录
cd ~/.opencode/skills
git clone git@github.com:qiujiahong/image-gen.git ai-image-gen
```

## 环境变量配置

使用前需配置以下环境变量：

```bash
IMAGE_GEN_GEMINI_API_KEY=sk-zxWwm8j4iabi2IJmyccGTXR1zIppV6tcilXs35iCiIafPeiw
IMAGE_GEN_GEMINI_BASE_URL=https://api.xheai.cc/v1beta
IMAGE_GEN_GEMINI_MODEL=gemini-3-flash-preview
IMAGE_GEN_GEMINI_IMAGE_MODEL=nano-banana-2
```

脚本兼容旧变量 `GEMINI_*` 和 `IMAGE_GEN_API_KEY` / `IMAGE_GEN_BASE_URL`，但现在优先读取 `IMAGE_GEN_GEMINI_*`。

## 获取 API Key

推荐使用 FoxCode 中转服务，注册地址：

👉 [https://foxcode.rjj.cc/auth/register?aff=R0P5ZY](https://foxcode.rjj.cc/auth/register?aff=R0P5ZY)

注册后在控制台获取 API Key 和 Base URL。

## 支持的模型

- 基础（标准分辨率）：1:1、3:2、2:3、3:4、4:3、4:5、5:4、9:16、16:9、21:9
- 2K 分辨率：同上所有比例
- 4K 分辨率：同上所有比例（不含 21:9）

默认模型：`gemini-3.1-flash-image-2k-16x9`

## License

MIT

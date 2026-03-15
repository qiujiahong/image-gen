# image-gen

AI 图像生成 Skill，支持文生图、图生图/编辑场景扩展，以及多种 Gemini / Gemini 兼容图像接口。
当前默认按 `IMAGE_GEN_GEMINI_*` 环境变量读取配置，并兼容 Gemini 原生返回与代理中转返回。

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

## 模型与返回兼容

当前默认图像模型：`nano-banana-2`

脚本支持两类接口返回：

1. **Gemini 原生格式**
   - 从 `candidates[].content.parts[].inlineData` 提取图片
2. **代理/中转格式**
   - 从 `data[0].url` 读取图片 URL 并自动下载到本地
   - 若返回 `b64_json`，也会尝试自动解码保存

说明：
- `IMAGE_GEN_GEMINI_MODEL` 可用于设置通用 Gemini 模型
- `IMAGE_GEN_GEMINI_IMAGE_MODEL` 用于设置实际出图模型
- 命令行传入 `--model` 时，优先使用命令行参数

## 示例

```bash
export IMAGE_GEN_GEMINI_API_KEY="your-api-key"
export IMAGE_GEN_GEMINI_BASE_URL="https://api.xheai.cc/v1beta"
export IMAGE_GEN_GEMINI_IMAGE_MODEL="nano-banana-2"

python3 scripts/generate_image.py \
  "一只坐在窗台上的橘猫，清晨阳光，写实摄影风格" \
  --output ./cat-test
```

如果接口返回的是图片 URL，脚本会自动下载并保存到本地。

## License

MIT

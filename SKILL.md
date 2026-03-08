---
name: image-gen
description: AI图像生成与编辑。支持文生图、图+文生图、风格转换。当用户要求画图、生成图片、编辑图片、图片风格转换时使用此 skill。支持多种比例（1:1、3:2、16:9、21:9 等）和分辨率（标准、2K、4K）。
---

# AI 图像生成

通过 Gemini Flash Image 模型实现图像生成和编辑。

## 环境变量

skill 通过以下环境变量获取 API 配置（不要硬编码）：

- `IMAGE_GEN_API_KEY` — API 密钥
- `IMAGE_GEN_BASE_URL` — API 基础地址

协议：Google Generative AI（google-generative-ai）

## 可用模型

默认模型：`gemini-3.1-flash-image-2k-16x9`

### 基础模型（标准分辨率）

| 模型 ID | 比例 |
|---------|------|
| gemini-3.1-flash-image | 1:1 |
| gemini-3.1-flash-image-3x2 | 3:2 |
| gemini-3.1-flash-image-2x3 | 2:3 |
| gemini-3.1-flash-image-3x4 | 3:4 |
| gemini-3.1-flash-image-4x3 | 4:3 |
| gemini-3.1-flash-image-4x5 | 4:5 |
| gemini-3.1-flash-image-5x4 | 5:4 |
| gemini-3.1-flash-image-9x16 | 9:16（竖屏）|
| gemini-3.1-flash-image-16x9 | 16:9（横屏）|
| gemini-3.1-flash-image-21x9 | 21:9（超宽）|

### 2K 分辨率

| 模型 ID | 比例 |
|---------|------|
| gemini-3.1-flash-image-2k | 1:1 |
| gemini-3.1-flash-image-2k-3x2 | 3:2 |
| gemini-3.1-flash-image-2k-2x3 | 2:3 |
| gemini-3.1-flash-image-2k-3x4 | 3:4 |
| gemini-3.1-flash-image-2k-4x3 | 4:3 |
| gemini-3.1-flash-image-2k-4x5 | 4:5 |
| gemini-3.1-flash-image-2k-5x4 | 5:4 |
| gemini-3.1-flash-image-2k-9x16 | 9:16 |
| gemini-3.1-flash-image-2k-16x9 | 16:9 |
| gemini-3.1-flash-image-2k-21x9 | 21:9 |

### 4K 分辨率

| 模型 ID | 比例 |
|---------|------|
| gemini-3.1-flash-image-4k | 1:1 |
| gemini-3.1-flash-image-4k-3x2 | 3:2 |
| gemini-3.1-flash-image-4k-2x3 | 2:3 |
| gemini-3.1-flash-image-4k-3x4 | 3:4 |
| gemini-3.1-flash-image-4k-4x3 | 4:3 |
| gemini-3.1-flash-image-4k-4x5 | 4:5 |
| gemini-3.1-flash-image-4k-5x4 | 5:4 |
| gemini-3.1-flash-image-4k-9x16 | 9:16 |
| gemini-3.1-flash-image-4k-16x9 | 16:9 |

## 使用流程

### 1. 选择模型

根据用户需求选择合适的模型：

- **用途决定比例**：手机壁纸→9:16，电脑壁纸→16:9/21:9，社交媒体→1:1，海报→3:4
- **用途决定分辨率**：预览/聊天→标准，印刷/展示→2K，大幅打印→4K
- **未指定时**：默认使用 `gemini-3.1-flash-image-2k-16x9`

### 2. 切换模型生成

使用 `session_status` 工具切换到目标图片模型，然后直接用自然语言描述生成图片。

```
session_status(model="foxcode/gemini-3.1-flash-image-2k-16x9")
```

### 3. 生图后切回

完成图片生成后，切回默认文本模型：

```
session_status(model="default")
```

## 提示词技巧

- 描述要具体：主体、场景、光线、风格、色调
- 参考风格：水彩、油画、赛博朋克、吉卜力、写实摄影等
- 图+文编辑：上传图片后描述修改要求（换背景、改风格、添加元素等）

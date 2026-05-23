# 八段锦导养平台（离线本地模型版）

## 1) 准备离线资源（仅第一次需要联网）
```powershell
cd c:\Users\86138\Desktop\八段锦
powershell -ExecutionPolicy Bypass -File .\download_offline_assets.ps1
```

下载完成后，后续运行可不依赖公网。

## 2) 启动本地服务
```powershell
python -m http.server 8000
```

## 3) 打开离线页面
`http://localhost:8000/index_offline.html`

## 4) 如果看到“离线模型加载失败”
请检查这4个文件是否存在：
- `assets/tasks-vision.bundle.mjs`
- `assets/models/pose_landmarker_lite.task`
- `assets/wasm/vision_wasm_internal.wasm`
- `assets/wasm/vision_wasm_nosimd_internal.wasm`

## 5) 功能
- 上传视频
- 人物识别框
- 33关键点识别
- 实时关键点坐标

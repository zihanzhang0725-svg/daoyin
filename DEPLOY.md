# 上线说明（Cloudflare Pages）

## 1. 本地已准备
- 默认入口：`index.html`
- 数字人素材：`avatar_assets/video4.mp4`
- 离线识别资源：`assets/`

## 2. 推送到 GitHub
```powershell
git init
git add .
git commit -m "Deploy-ready web app"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

## 3. Cloudflare Pages
- Workers & Pages -> Create -> Pages -> Connect to Git
- 选择仓库
- Framework preset: None
- Build command: (留空)
- Build output directory: /
- Deploy

## 4. 访问
部署后域名示例：`https://<project>.pages.dev`

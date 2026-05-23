$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force "assets" | Out-Null
New-Item -ItemType Directory -Force "assets\models" | Out-Null
New-Item -ItemType Directory -Force "assets\wasm" | Out-Null

Write-Host "Downloading tasks-vision bundle..."
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs" -OutFile "assets\tasks-vision.bundle.mjs"

Write-Host "Downloading pose model..."
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task" -OutFile "assets\models\pose_landmarker_lite.task"

Write-Host "Downloading wasm runtime files..."
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm/vision_wasm_internal.wasm" -OutFile "assets\wasm\vision_wasm_internal.wasm"
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm/vision_wasm_nosimd_internal.wasm" -OutFile "assets\wasm\vision_wasm_nosimd_internal.wasm"
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm/vision_wasm_internal.js" -OutFile "assets\wasm\vision_wasm_internal.js"
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm/vision_wasm_nosimd_internal.js" -OutFile "assets\wasm\vision_wasm_nosimd_internal.js"

Write-Host "Done. Offline assets are ready."

import tempfile
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

st.set_page_config(page_title="八段锦导养平台 - 姿态识别", layout="wide")
st.title("八段锦导养平台：视频人体识别与关键点坐标")
st.caption("上传视频后，系统会检测人物框、姿态关键点，并实时展示坐标。")

with st.sidebar:
    st.header("识别参数")
    detect_conf = st.slider("最小检测置信度", 0.1, 1.0, 0.5, 0.05)
    track_conf = st.slider("最小跟踪置信度", 0.1, 1.0, 0.5, 0.05)
    display_fps = st.slider("显示帧率（节流）", 5, 30, 15, 1)
    show_landmark_index = st.checkbox("显示关键点编号", value=True)

uploaded_file = st.file_uploader(
    "上传视频文件", type=["mp4", "mov", "avi", "mkv"]
)

if uploaded_file is None:
    st.info("请先上传一段视频。")
    st.stop()

suffix = Path(uploaded_file.name).suffix or ".mp4"
with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
    tmp.write(uploaded_file.read())
    video_path = tmp.name

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    st.error("视频打开失败，请更换视频格式后重试。")
    st.stop()

source_fps = cap.get(cv2.CAP_PROP_FPS)
if source_fps <= 0:
    source_fps = 25.0
step = max(int(source_fps / display_fps), 1)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

col_left, col_right = st.columns([2, 1])
frame_area = col_left.empty()
coords_area = col_right.empty()
progress = st.progress(0)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_idx = 0

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=detect_conf,
    min_tracking_confidence=track_conf,
) as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        if frame_idx % step != 0:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        h, w, _ = frame.shape
        rows = []

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_draw.DrawingSpec(
                    color=(0, 255, 0), thickness=2, circle_radius=2
                ),
                connection_drawing_spec=mp_draw.DrawingSpec(
                    color=(255, 180, 0), thickness=2
                ),
            )

            xs = []
            ys = []
            for i, lm in enumerate(results.pose_landmarks.landmark):
                x_px = int(lm.x * w)
                y_px = int(lm.y * h)
                xs.append(x_px)
                ys.append(y_px)

                rows.append(
                    {
                        "id": i,
                        "name": mp_pose.PoseLandmark(i).name,
                        "x": x_px,
                        "y": y_px,
                        "z": round(float(lm.z), 4),
                        "visibility": round(float(lm.visibility), 4),
                    }
                )

                if show_landmark_index:
                    cv2.putText(
                        frame,
                        str(i),
                        (x_px + 3, y_px - 3),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

            # 用关键点外接矩形作为人物识别框
            x_min = max(min(xs), 0)
            x_max = min(max(xs), w - 1)
            y_min = max(min(ys), 0)
            y_max = min(max(ys), h - 1)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
            cv2.putText(
                frame,
                "Person",
                (x_min, max(y_min - 8, 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        frame_area.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

        if rows:
            coords_area.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            coords_area.info("当前帧未检测到人体关键点")

        if total_frames > 0:
            progress.progress(min(frame_idx / total_frames, 1.0))

cap.release()
progress.progress(1.0)
st.success("视频处理完成。")

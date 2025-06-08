import streamlit as st
from generate_video import generate_jedag_video

st.title("🎬 Jedag-Jedug Video Generator")

video = st.file_uploader("📂 Upload video mentah (.mp4)", type="mp4")
preset = st.file_uploader("📄 Upload preset JSON (.json)", type="json")

if st.button("▶️ Generate") and video and preset:
    with st.spinner("🎞️ Rendering video..."):
        output_path = generate_jedag_video(video, preset)
    st.success("✅ Selesai! Video berhasil dirender.")
    st.video(output_path)
    with open(output_path, "rb") as file:
        st.download_button("⬇️ Download Video", file, file_name="generated_jedag.mp4")

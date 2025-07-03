import streamlit as st
import pandas as pd
import json

st.title("☢ MSREⅡ 控制面板")

st.sidebar.header("控制参数设置")
T_ref = st.sidebar.slider("目标出口温度 T_ref [K]", 800, 1100, 950)
n_ref = st.sidebar.slider("目标中子功率 n_ref", 0.0, 2.0, 1.0)

if st.sidebar.button("提交控制参数"):
    params = {"T_ref": T_ref, "n_ref": n_ref}
    with open("external_input.json", "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2)
    st.sidebar.success("控制参数已更新 ✅")

st.subheader("温度与功率演化结果")
try:
    df = pd.read_csv("outputs/run1/scalars.csv")
    st.line_chart(df.set_index("time")[["T_out", "n"]])
except Exception:
    st.info("尚未生成仿真结果数据，请先运行仿真程序")

st.markdown("---")
st.caption("© MSREⅡ 仿真平台 by 鸿强")

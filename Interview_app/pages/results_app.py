import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("📊 アンケート：受講前後比較")

# ディレクトリパス
pre_path = "data/pre"
post_path = "data/post"

# 存在確認＆初期化（Cloud上で確実に存在しないときでも対応）
if not os.path.exists(pre_path):
    st.warning("⚠️ 'data/pre' フォルダが存在しません。まだ誰もアンケートに回答していないか、アップロードに失敗している可能性があります。")
    pre_ids = []
else:
    pre_ids = [f[:-4] for f in os.listdir(pre_path) if f.endswith(".csv")]

if not os.path.exists(post_path):
    st.warning("⚠️ 'data/post' フォルダが存在しません。まだ誰も受講後アンケートに回答していないか、アップロードに失敗している可能性があります。")
    post_ids = []
else:
    post_ids = [f[:-4] for f in os.listdir(post_path) if f.endswith(".csv")]

valid_ids = list(set(pre_ids) & set(post_ids))

if not valid_ids:
    st.warning("受講前後データが揃っていません。")
else:
    student_id = st.selectbox("比較する受講者を選んでください", sorted(valid_ids))

    # CSV読み込み & 列名変換
    df_pre = pd.read_csv(f"data/pre/{student_id}.csv").rename(columns={"スコア": "受講前"})
    df_post = pd.read_csv(f"data/post/{student_id}.csv").rename(columns={"スコア": "受講後"})

    # 結合
    df = pd.merge(df_pre, df_post, on=["ID", "観点詳細"])
    df = df.sort_values("観点詳細")
    df["変化量"] = df["受講後"] - df["受講前"]

    # レーダーチャート
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df["受講前"],
        theta=df["観点詳細"],
        fill='toself',
        name='受講前'
    ))
    fig.add_trace(go.Scatterpolar(
        r=df["受講後"],
        theta=df["観点詳細"],
        fill='toself',
        name='受講後'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 4])),
        showlegend=True
    )
    st.plotly_chart(fig)

    # 数値表示
    st.dataframe(df[["観点詳細", "受講前", "受講後", "変化量"]])

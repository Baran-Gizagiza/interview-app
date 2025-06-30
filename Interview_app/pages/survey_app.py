import streamlit as st
import pandas as pd
import os

st.title("🧭 自己認識：アンケート")

# 1. 基本情報の入力
student_id = st.text_input("あなたのお名前またはIDを入力してください")
survey_type = st.radio("アンケートの種類を選んでください", ["受講前", "受講後"])

# 2. 質問定義（細分化された観点）
questions = {
    "人間関係形成能力_自他理解": "自分と他者の考えや感情の違いを理解できている",
    "人間関係形成能力_コミュニケーション": "人と円滑にコミュニケーションを取ることができる",
    "情報活用能力_情報収集": "必要な情報を自分で集める力がある",
    "情報活用能力_職業理解": "将来の職業や仕事について情報を持っている",
    "将来設計能力_役割認識": "自分の役割や立場を理解して行動できる",
    "将来設計能力_計画実行": "将来に向けた計画を立て、行動している",
    "意思決定能力_選択": "自分に必要な選択を自信を持ってできる",
    "意思決定能力_課題解決": "問題に直面したときに解決方法を考えて行動できる"
}

st.subheader("以下の各項目について、現在の自分の状態に近いものを選んでください（1: まったくそう思わない ～ 4: とてもそう思う）")

# 3. 回答入力UI
responses = {}
for key, question in questions.items():
#     responses[key] = st.slider(question, 1, 4, 2)

    responses[key] = st.radio(
        question,
        options=[1, 2, 3, 4],
        index=1,
        horizontal=True
    )

# 4. 保存処理
if st.button("回答を送信する"):
    if student_id.strip() == "":
        st.warning("名前またはIDを入力してください。")
    else:
        # 保存フォルダとファイル名を定義
        folder = "data/pre" if survey_type == "受講前" else "data/post"
        os.makedirs(folder, exist_ok=True)
        file_path = f"{folder}/{student_id}.csv"

        # 保存用データフレーム
        df = pd.DataFrame([{
            "ID": student_id,
            "観点詳細": key,
            "スコア": responses[key]
        } for key in responses])

        df.to_csv(file_path, index=False)
        st.success(f"{survey_type} アンケートを {folder}/ に保存しました！")

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from utils.transcription import GladiaAPI
from utils.text_formatter import GeminiFormatter
from utils.voicevox import VoiceVoxAPI

# 環境変数を読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="TikTok Re-Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - TikTokスタイルのボタンとUI
st.markdown("""
<style>
    /* TikTokカラー: シアン #00f2ea, ピンク #fe2c55, 黒背景 */

    /* ダークテーマの背景 */
    .stApp {
        background: #000000;
        color: #ffffff;
    }

    /* ヘッダースタイル */
    h1 {
        color: #ffffff !important;
        text-shadow:
            2px 2px 0px #fe2c55,
            -2px -2px 0px #00f2ea;
        font-weight: bold !important;
    }

    h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 242, 234, 0.5);
    }

    /* 全てのボタンをSTARTボタンデザインに統一 - コンパクト版 */
    .stButton > button {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #00f2ea !important;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.5);
        transition: all 0.3s ease;
        width: 100%;
        min-height: 45px;
    }

    .stButton > button:hover {
        background: #1a1a1a !important;
        border: 3px solid #00f2ea !important;
        color: #00f2ea !important;
        box-shadow:
            0 0 40px rgba(0, 242, 234, 1),
            0 0 60px rgba(0, 242, 234, 0.6),
            inset 0 0 20px rgba(0, 242, 234, 0.2);
        transform: translateY(-3px) scale(1.02);
    }

    /* DOWNLOAD TEXTボタン - コンパクト版 */
    .stDownloadButton > button {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #00f2ea !important;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.5);
        transition: all 0.25s ease;
        width: 100%;
        min-height: 45px;
    }

    .stDownloadButton > button:hover {
        background: #1a1a1a !important;
        border: 3px solid #00f2ea !important;
        color: #00f2ea !important;
        box-shadow:
            0 0 40px rgba(0, 242, 234, 1),
            0 0 60px rgba(0, 242, 234, 0.6),
            inset 0 0 20px rgba(0, 242, 234, 0.2);
        transform: translateY(-3px) scale(1.02);
    }

    /* テキストエリア - コンパクト版＋目立つカーソル */
    .stTextArea textarea {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
        caret-color: #00f2ea !important;
        padding: 10px !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    /* テキストインプット - コンパクト版＋目立つカーソル */
    .stTextInput input {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
        caret-color: #00f2ea !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }

    /* セレクトボックス */
    .stSelectbox > div > div {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
    }

    /* スライダー */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00f2ea 0%, #fe2c55 100%) !important;
    }

    /* インフォボックス */
    .stInfo {
        background: rgba(0, 242, 234, 0.1) !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
    }

    /* ファイルアップローダー */
    .stFileUploader {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    /* オーディオプレイヤー */
    audio {
        width: 100% !important;
        filter:
            drop-shadow(0 0 10px rgba(0, 242, 234, 0.5))
            drop-shadow(0 0 20px rgba(254, 44, 85, 0.3));
    }

    /* タブスタイル - コンパクト版 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent !important;
        padding: 15px 10px 20px 10px;
        border: none !important;
        border-bottom: none !important;
        display: flex !important;
        flex-direction: row !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        height: 45px !important;
        min-height: 45px !important;
        padding: 12px 30px !important;
        background: #000000 !important;
        border: 2px solid #00f2ea !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.5) !important;
        transition: all 0.25s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #1a1a1a !important;
        border: 3px solid #00f2ea !important;
        color: #00f2ea !important;
        box-shadow:
            0 0 40px rgba(0, 242, 234, 1),
            0 0 60px rgba(0, 242, 234, 0.6),
            inset 0 0 20px rgba(0, 242, 234, 0.2) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }

    .stTabs [aria-selected="true"] {
        background: #000000 !important;
        border: 2px solid #00f2ea !important;
        color: white !important;
        box-shadow: 0 0 25px rgba(0, 242, 234, 0.7) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 30px;
    }

    /* すべてのボーダーと装飾を削除 */
    .stTabs [data-baseweb="tab-list"]::after,
    .stTabs [data-baseweb="tab-list"]::before,
    .stTabs [data-baseweb="tab"]::after,
    .stTabs [data-baseweb="tab"]::before,
    .stTabs [aria-selected="true"]::after,
    .stTabs [aria-selected="true"]::before {
        display: none !important;
        content: none !important;
    }

    .stTabs,
    .stTabs *,
    .stTabs [role="tablist"],
    .stTabs [role="tablist"] *,
    button[role="tab"],
    button[role="tab"] *,
    div[data-baseweb="tab-border"],
    div[data-baseweb="tab-highlight"] {
        border: none !important;
        border-bottom: none !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }

    div[data-baseweb="tab-border"],
    div[data-baseweb="tab-highlight"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
    }

    .stTabs > div,
    .stTabs > div > div,
    .stTabs > div > div > div {
        border-bottom: none !important;
    }
</style>
""", unsafe_allow_html=True)

# セッションステートの初期化
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = None
if 'formatted_text' not in st.session_state:
    st.session_state.formatted_text = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None
if 'sample_audio' not in st.session_state:
    st.session_state.sample_audio = None

# タイトル
st.title("🎬 TikTok Re-Editor")
st.markdown("動画をアップロードして、文字起こし → 整形 → 音声合成を自動実行")

# サイドバー：API設定
with st.sidebar:
    st.header("⚙️ API設定")
    st.markdown("各APIキーを入力してください")

    # .envファイルから読み込み（ローカル開発用）
    env_gladia = os.getenv("GLADIA_API_KEY", "")
    env_gemini = os.getenv("GEMINI_API_KEY", "")
    env_voicevox = os.getenv("VOICEVOX_API_URL", "http://localhost:50021")

    # APIキー入力
    gladia_api_key = st.text_input(
        "🎤 Gladia API Key",
        value=env_gladia,
        type="password",
        help="文字起こし用APIキー（動画アップロード時のみ必要）"
    )

    gemini_api_key = st.text_input(
        "✨ Gemini API Key",
        value=env_gemini,
        type="password",
        help="テキスト整形・ファイル名生成用APIキー（動画アップロード時のみ必要）"
    )

    voicevox_url = st.text_input(
        "🎙️ VOICEVOX URL",
        value=env_voicevox,
        help="通常は変更不要。あなたのPCでVOICEVOXを起動してください。"
    )

    st.markdown("---")
    st.markdown("### 📚 APIキーの取得方法")
    st.markdown("- **Gladia API**: [gladia.io](https://www.gladia.io/)")
    st.markdown("- **Gemini API**: [ai.google.dev](https://ai.google.dev/)")
    st.markdown("- **VOICEVOX**: [voicevox.hiroshiba.jp](https://voicevox.hiroshiba.jp/)")

    st.markdown("---")
    st.info("💡 テキストファイルから生成する場合、Gladia/Gemini APIは不要です")

# APIクライアントの初期化
gladia = GladiaAPI(gladia_api_key) if gladia_api_key else None
gemini = GeminiFormatter(gemini_api_key) if gemini_api_key else None
voicevox = VoiceVoxAPI(voicevox_url)

# セクション1: 入力ソース選択
st.header("📥 1. 入力ソース選択")

# タブで動画とテキストを切り替え
tab1, tab2 = st.tabs(["📹 動画から生成", "📄 テキストから生成"])

with tab1:
    st.subheader("動画アップロード")

    uploaded_file = st.file_uploader(
        "動画ファイルを選択してください",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="video_uploader"
    )

    if uploaded_file is not None:
        # 動画を一時ファイルとして保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        st.info(f"📁 アップロードされたファイル: {uploaded_file.name}")

        # 文字起こしボタン
        if st.button("START...", key="transcribe_btn"):
            # APIキーチェック
            if not gladia_api_key or not gemini_api_key:
                st.error("⚠️ サイドバーでGladia APIキーとGemini APIキーを入力してください")
                st.stop()

            with st.status("処理中...", expanded=True) as status:
                st.write("📤 動画をアップロード中...")
                audio_url = gladia.upload_file(tmp_file_path)

                if audio_url:
                    st.write("✅ アップロード完了")
                    st.write("🎤 文字起こし中... (数分かかる場合があります)")

                    transcribed = gladia.transcribe(audio_url, language="ja")

                    if transcribed:
                        st.session_state.transcribed_text = transcribed
                        st.write("✅ 文字起こし完了")

                        st.write("✏️ テキスト整形中...")
                        formatted = gemini.format_text(transcribed)

                        if formatted:
                            st.session_state.formatted_text = formatted
                            st.write("✅ テキスト整形完了")

                            st.write("📝 ファイル名生成中...")
                            filename = gemini.generate_filename(formatted)

                            if filename:
                                st.session_state.filename = filename
                                st.write("✅ ファイル名生成完了")
                                status.update(label="✅ すべての処理が完了しました！", state="complete")
                            else:
                                st.error("ファイル名生成に失敗しました")
                        else:
                            st.error("テキスト整形に失敗しました")
                    else:
                        st.error("文字起こしに失敗しました")
                else:
                    st.error("動画のアップロードに失敗しました")

        # 一時ファイルを削除
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

with tab2:
    st.subheader("テキストファイルアップロード")

    text_file = st.file_uploader(
        "テキストファイルを選択してください (.txt)",
        type=["txt"],
        key="text_file_uploader"
    )

    if text_file is not None:
        st.info(f"📁 アップロードされたファイル: {text_file.name}")

        # テキスト処理ボタン
        if st.button("START...", key="text_process_btn"):
            with st.status("処理中...", expanded=True) as status:
                st.write("📄 テキストファイルを読み込み中...")

                try:
                    # テキストファイルを読み込み
                    raw_text = text_file.read().decode('utf-8', errors='replace')

                    if not raw_text.strip():
                        st.error("⚠️ テキストファイルが空です")
                    else:
                        # テキストをそのまま整形済みとして扱う
                        st.session_state.transcribed_text = raw_text
                        st.session_state.formatted_text = raw_text
                        st.write("✅ テキスト読み込み完了")

                        # ファイル名から拡張子を除いたものを使用
                        import os
                        filename = os.path.splitext(text_file.name)[0]
                        st.session_state.filename = filename
                        st.write("✅ ファイル名設定完了")

                        status.update(label="✅ すべての処理が完了しました！", state="complete")

                except Exception as e:
                    st.error(f"❌ テキスト読み込みエラー: {str(e)}")

# セクション2: 整形済みテキスト表示
if st.session_state.formatted_text:
    st.header("📝 2. 整形済みテキスト")

    # テキストエリアの初期値を設定
    if "text_editor" not in st.session_state:
        st.session_state.text_editor = st.session_state.formatted_text

    # 編集可能なテキストエリア
    st.text_area(
        "整形されたテキスト（編集可能）",
        height=300,
        key="text_editor"
    )

    # テキストダウンロードボタン（テキストエリアの直後）
    st.subheader("💾 テキストをダウンロード")

    # ファイル名の確認・編集
    if "filename" not in st.session_state or not st.session_state.filename:
        st.session_state.filename = "output"

    final_filename = st.text_input(
        "ファイル名（編集可能）",
        value=st.session_state.filename,
        key="filename_input"
    )

    # テキストファイルダウンロード
    st.download_button(
        label="DOWNLOAD TEXT",
        data=st.session_state.text_editor,
        file_name=f"{final_filename}.txt",
        mime="text/plain",
        key="download_text"
    )

    # セクション3: VOICEVOX設定
    st.header("🎙️ 3. 音声合成設定")

    # スピーカー一覧を取得
    speakers = voicevox.get_speakers()

    if speakers:
        # スピーカー名のリストを作成
        speaker_names = [speaker.get("name", "") for speaker in speakers]

        # 初期値を「青山流星」に設定（存在する場合）
        default_index = 0
        if "青山龍星" in speaker_names:
            default_index = speaker_names.index("青山龍星")
        elif "青山流星" in speaker_names:
            default_index = speaker_names.index("青山流星")

        col1, col2 = st.columns(2)

        with col1:
            selected_speaker_name = st.selectbox(
                "🎭 キャラクター選択",
                speaker_names,
                index=default_index
            )

        # 選択されたスピーカーのスタイルを取得
        selected_speaker = next(
            (s for s in speakers if s.get("name") == selected_speaker_name),
            None
        )

        if selected_speaker:
            styles = selected_speaker.get("styles", [])
            style_names = [style.get("name", "") for style in styles]

            with col2:
                selected_style_name = st.selectbox(
                    "🎨 スタイル選択",
                    style_names,
                    index=0
                )

            # スピーカーIDを取得
            speaker_id = voicevox.find_speaker_id(
                speakers,
                selected_speaker_name,
                selected_style_name
            )

            # キャラクター試聴ボタン
            if st.button("PREVIEW VOICE", key="sample_btn"):
                with st.spinner("サンプル音声を生成中..."):
                    sample_audio = voicevox.generate_sample_voice(speaker_id)
                    if sample_audio:
                        st.session_state.sample_audio = sample_audio
                        st.success("✅ サンプル音声を生成しました")
                    else:
                        st.error("サンプル音声の生成に失敗しました")

            # サンプル音声プレイヤー
            if st.session_state.sample_audio:
                st.audio(st.session_state.sample_audio, format="audio/wav")

            # 話速設定
            speed = st.slider(
                "⚡ 話速（Speed）",
                min_value=0.5,
                max_value=2.0,
                value=1.2,
                step=0.1
            )

            # 音声生成ボタン
            if st.button("GENERATE", key="generate_btn"):
                with st.spinner("音声を生成中... (時間がかかる場合があります)"):
                    # 編集されたテキストを使用
                    current_text = st.session_state.get("text_editor", st.session_state.formatted_text)
                    audio_data = voicevox.generate_voice(
                        current_text,
                        speaker_id,
                        speed
                    )

                    if audio_data:
                        st.session_state.generated_audio = audio_data
                        st.success("✅ 音声を生成しました！")
                    else:
                        st.error("音声生成に失敗しました")

            # 生成された音声のプレビュー
            if st.session_state.generated_audio:
                st.subheader("🎧 生成された音声")
                st.audio(st.session_state.generated_audio, format="audio/wav")

                # 音声ダウンロードボタン
                st.subheader("💾 音声をダウンロード")
                audio_filename = st.session_state.get("filename_input", st.session_state.get("filename", "output"))
                st.download_button(
                    label="DOWNLOAD AUDIO",
                    data=st.session_state.generated_audio,
                    file_name=f"{audio_filename}.wav",
                    mime="audio/wav",
                    key="download_audio"
                )

    else:
        st.error("⚠️ VOICEVOXに接続できません")
        st.warning("""
        **VOICEVOXを使用するには：**
        1. あなたのPC（ローカル環境）でVOICEVOXアプリを起動してください
        2. VOICEVOXが完全に起動するまで待ってください
        3. このページをリロードしてください

        📥 VOICEVOXダウンロード: https://voicevox.hiroshiba.jp/
        """)

# フッター
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, Gladia API, Gemini API, and VOICEVOX")

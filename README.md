# 🎬 TikTok Re-Editor VOICEVOX

動画やテキストファイルから「文字起こし → 14文字整形 → 音声合成」を自動実行するStreamlitアプリ。

## ✨ 機能

### 📹 動画から生成
- **動画文字起こし**: Gladia APIを使用した自動文字起こし
- **テキスト整形**: Gemini APIで14文字/行に整形（句読点と改行のみ、内容は変更なし）
- **ファイル名生成**: Gemini APIで適切なファイル名を自動生成
- **音声合成**: VOICEVOXを使用した音声生成

### 📄 テキストファイルから生成（NEW）
- テキストファイル（.txt）を直接アップロード
- Gemini API不要でクォータ節約
- 整形なしでそのまま音声生成

### 🎙️ 共通機能
- **プレビュー機能**: キャラクター試聴、生成音声試聴
- **編集可能**: 整形済みテキストを手動編集可能
- **ダウンロード**: テキストと音声を両方ダウンロード可能

## 🚀 クイックスタート

### 方法1: Streamlit Community Cloud（推奨・無料）

**このアプリはWebで公開されています！**

1. 📥 **VOICEVOXをダウンロード**
   - [voicevox.hiroshiba.jp](https://voicevox.hiroshiba.jp/)からダウンロード
   - あなたのPC（ローカル環境）にインストール

2. 🎙️ **VOICEVOXを起動**
   - VOICEVOXアプリを起動（バックグラウンドで実行）

3. 🌐 **ブラウザでアプリにアクセス**
   - このアプリのURLを開く
   - サイドバーでAPIキーを入力（初回のみ）
     - **動画から生成**: Gladia API + Gemini API が必要
     - **テキストから生成**: APIキー不要で使えます！

4. ✅ **完了！**
   - テキストファイルから生成なら今すぐ使えます

### 方法2: ローカル環境で実行

**詳しい手順は [`セットアップ手順.md`](./セットアップ手順.md) を参照してください。**

<details>
<summary>クリックして手順を表示</summary>

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/yourusername/TikTok-Re-Editor-VOICEVOX.git
   cd TikTok-Re-Editor-VOICEVOX
   ```

2. **パッケージをインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **環境変数を設定（オプション）**
   ```bash
   cp .env.example .env
   # .envファイルを編集してAPIキーを設定
   ```
   ※ サイドバーでAPIキーを入力することもできます

4. **VOICEVOXを起動**
   - VOICEVOXアプリケーションを起動
   - `http://localhost:50021` で待機

5. **アプリを起動**
   ```bash
   streamlit run app.py
   ```

6. **ブラウザで開く**
   - 自動的にブラウザが開きます
   - 開かない場合は `http://localhost:8501` にアクセス

</details>

---

## 📖 使用方法

### 📹 動画から生成する場合

1. サイドバーで **Gladia API** と **Gemini API** キーを入力
2. **「動画から生成」タブ**を選択
3. 動画ファイル（mp4, mov, avi, mkv, webm）をアップロード
4. **「START」ボタン**をクリック
5. 自動的に文字起こし・整形が実行されます
6. テキストを編集（必要に応じて）
7. VOICEVOXのキャラクターと話速を選択
8. **「GENERATE」ボタン**で音声生成
9. テキストと音声をダウンロード

### 📄 テキストファイルから生成する場合

1. **「テキストから生成」タブ**を選択
2. テキストファイル（.txt）をアップロード
3. **「START」ボタン**をクリック
4. テキストを編集（必要に応じて）
5. VOICEVOXのキャラクターと話速を選択
6. **「GENERATE」ボタン**で音声生成
7. テキストと音声をダウンロード

💡 **ヒント**: テキストファイルからの生成は **API不要** で使えます！

---

## 🔑 必要なAPI

| API | 用途 | 必要なタイミング | 取得方法 |
|-----|------|------------------|----------|
| **Gladia API** | 動画の文字起こし | 動画から生成する時のみ | [gladia.io](https://www.gladia.io/) |
| **Gemini API** | テキスト整形・ファイル名生成 | 動画から生成する時のみ | [ai.google.dev](https://ai.google.dev/) |
| **VOICEVOX** | 音声合成 | 常に必要（ローカル実行） | [voicevox.hiroshiba.jp](https://voicevox.hiroshiba.jp/) |

⚠️ **重要**:
- テキストファイルから生成する場合、Gladia/Gemini APIは不要です
- VOICEVOXは **あなたのPC** で起動する必要があります

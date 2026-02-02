from google import genai
import os
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込みます
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY が設定されていません！")

# Geminiクライアントの初期化
client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    """
    指定されたプロンプトをGeminiに送信し、返答を返します。
    """
    try:
        # ご希望の最新モデル gemini-3-flash-preview を使用
        res = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        
        # 応答テキストが存在するかチェックし、あれば返却
        if res and res.text:
            return res.text
        
        # 空のレスポンスが返ってきた場合
        return "……言葉が見つかりませんでした"
        
    except Exception as e:
        # ターミナルに具体的なエラー理由を表示（デバッグ用）
        print(f"--- Gemini API Error ---")
        print(f"詳細: {e}")
        # プログラムを止めず、Discord側にはエラーを通知
        return f"……沈黙です。（エラーが発生しました）"
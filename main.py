import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

# [흐름] 1. 비밀 서랍(.env)에서 API 키 꺼내기
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# [보안] API 키가 없으면 미리 경고하기
if not API_KEY:
    print("⚠️ 경고: GEMINI_API_KEY가 .env 파일에 없거나 읽을 수 없습니다!")

# 전역 변수로 모델을 저장합니다.
available_model = None

def find_best_model():
    """사용 가능한 최적의 모델을 찾아 반환합니다."""
    if not API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        # 구글 서버에서 사용 가능한 모델 목록을 가져옵니다.
        models = genai.list_models()
        for m in models:
            # 대화형 답변(generateContent)이 가능한 모델 중 'flash'나 'pro'가 들어간 것을 찾습니다.
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name:
                    print(f"✅ 사용 가능한 모델 발견: {m.name}")
                    return m.name
        return None
    except Exception as e:
        print(f"❌ 모델 목록 확인 실패: {e}")
        return None

app = FastAPI()

# [구조] 2. 브라우저 접근 허용 (CORS) 설정
# 이 설정을 해야 프런트엔드에서 백엔드에게 데이터를 요청할 수 있습니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"], # 모든 방식(GET, POST 등) 허용
    allow_headers=["*"], # 모든 헤더 허용
)

# [로직] 3. AI에게 줄 성격 매뉴얼
SYSTEM_INSTRUCTION = """
너는 'AI 할 일 관리자'야. 사용자가 할 일을 입력하면,
다음 두 가지 정보를 분석해서 [중요도, 카테고리] 형식으로 알려줘.
1. 중요도: 높음, 중간, 낮음
2. 카테고리: 업무, 개인, 공부, 기타

반드시 [중요도: OO, 카테고리: OO] 형식으로만 대답해.
"""

@app.get("/")
def root():
    model_name = find_best_model()
    return {
        "message": "AI ToDo Manager 실행 중!",
        "detected_model": model_name if model_name else "없음 (API Key 확인 필요)"
    }

@app.get("/analyze")
async def analyze_todo(task: str):
    if not API_KEY:
        return {"error": "API Key 없음"}

    # 매번 호출할 때마다 최적의 모델을 찾습니다 (에러 방지용)
    model_name = find_best_model()
    if not model_name:
        return {"error": "사용 가능한 AI 모델을 찾을 수 없습니다. API Key 권한을 확인하세요."}

    prompt = f"{SYSTEM_INSTRUCTION}\n\n사용자 할 일: {task}"
    
    try:
        current_model = genai.GenerativeModel(model_name)
        response = current_model.generate_content(prompt)
        return {
            "user_task": task,
            "ai_analysis": response.text.strip(),
            "model_used": model_name
        }
    except Exception as e:
        return {"error": f"분석 실패: {str(e)}"}

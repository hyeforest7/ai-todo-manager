from fastapi import FastAPI
import logging

# [구조] 1. 서버의 입구 만들기
app = FastAPI()

# [로직] 2. AI에게 줄 성격 매뉴얼 (Prompt)
SYSTEM_INSTRUCTION = """
너는 'AI 할 일 관리자'야. 사용자가 할 일을 입력하면,
다음 두 가지 정보를 분석해서 [중요도, 카테고리] 형식으로 알려줘.

1. 중요도: 높음, 중간, 낮음 중 하나
2. 카테고리: 업무, 개인, 공부, 기타 중 하나

답변 예시: [중요도: 높음, 카테고리: 업무]
"""

# [흐름] 3. 사용자의 할 일을 분석하는 기능 (API)
@app.get("/")
def root():
    return {"message": "AI ToDo Manager 서버가 정상입니다!"}

@app.get("/analyze")
def analyze_todo(task: str):
    # 실제 AI 연결은 다음 단계에서 하고, 지금은 '흐름'만 봅니다!
    print(f"사용자가 보낸 할 일: {task}")
    
    # 가상의 결과 (나중에 AI가 이 자리에 진짜 답을 줄 거예요)
    result = "[중요도: 높음, 카테고리: 개인]"
    
    return {
        "user_task": task,
        "ai_analysis": result
    }

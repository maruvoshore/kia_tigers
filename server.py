from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 소크라테스식 데이터베이스 (예시: 1000번 A+B 문제)
# 실제 서비스에선 이 내용을 LLM(GPT)이 실시간으로 생성하게 됩니다.
socratic_db = {
    "1000": [
        {
            "step": "1. 문제 재정의",
            "question": "이 문제에서 진짜로 구해야 하는 값은 무엇인가요?\n입력받은 두 숫자를 그대로 출력하는 게 아니라, 그 사이의 '관계'를 계산해야 하지 않나요?"
        },
        {
            "step": "2. 제약 조건 질문",
            "question": "입력되는 A와 B는 0보다 크고 10보다 작습니다.\n이 정도 크기라면, 데이터 타입(int, long 등)에 신경 쓸 필요가 있을까요?"
        },
        {
            "step": "3. 반복 구조 유도",
            "question": "이 문제는 반복이 필요한가요, 아니면 단 한 번의 연산으로 끝나는가요?\n입력을 받고 -> 계산하고 -> 출력하는 흐름을 그려보세요."
        },
        {
            "step": "4. 반례 질문",
            "question": "만약 A가 1이고 B가 2라면 3이 나와야 합니다.\n그런데 예제 입력과 다른 숫자를 넣어도 항상 정답이 나오나요?"
        },
        {
            "step": "5. 알고리즘 귀결",
            "question": "이 문제는 복잡한 알고리즘이 필요한가요?\n단순한 '사칙연산 구현' 문제인지 확인해 보세요."
        }
    ],
    "2557": [
        {"step": "1. 문제 재정의", "question": "컴퓨터 화면에 특정 문장을 띄우는 것이 목표입니다. 어떤 함수가 필요할까요?"},
        {"step": "2. 제약 조건", "question": "대소문자가 정확해야 합니다. 'Hello World'와 'Hello world'는 다릅니다."},
        {"step": "5. 결론", "question": "Python의 print 함수 사용법을 정확히 알고 있나요?"}
    ]
}

@app.get("/hint/{problem_id}")
def get_socratic_hint(problem_id: str):
    # 해당 문제의 소크라테스 질문 리스트를 반환
    hints = socratic_db.get(problem_id)

    if not hints:
        return {"found": False, "msg": "🤔 흠, 이 문제는 아직 소크라테스 선생님이 분석하지 못했네요."}

    return {"found": True, "hints": hints}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

app = FastAPI()

# CORS 설정 (이건 그대로)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Render 환경변수에서 API 키를 가져옵니다. (코드에 직접 적지 마세요!)
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/hint/{problem_id}")
async def get_socratic_hint(problem_id: str):
    print(f"🔍 문제 분석 요청 들어옴: {problem_id}번")

    # GPT에게 보낼 프롬프트 (소크라테스 빙의)
    prompt = f"""
    당신은 '소크라테스' 교육 방식의 알고리즘 선생님입니다.
    학생이 백준 온라인 저지(BOJ) 문제 번호 '{problem_id}'번을 풀다가 막혔습니다.

    절대로 정답 코드나 직접적인 풀이를 주지 마세요.
    대신, 학생이 스스로 생각할 수 있도록 5단계의 질문을 던지세요.

    반드시 아래 JSON 포맷으로만 응답해주세요:
    [
        {{"step": "1. 문제 재정의", "question": "질문 내용..."}},
        {{"step": "2. 제약 조건 확인", "question": "질문 내용..."}},
        {{"step": "3. 접근 방식 유도", "question": "질문 내용..."}},
        {{"step": "4. 엣지 케이스 점검", "question": "질문 내용..."}},
        {{"step": "5. 알고리즘 힌트", "question": "질문 내용..."}}
    ]
    한국어로, 친절하지만 논리적으로 질문하세요.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # 가성비 좋은 모델 (gpt-3.5-turbo보다 똑똑하고 저렴)
            messages=[
                {"role": "system", "content": "You are a helpful Socratic tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        # GPT가 준 텍스트를 JSON으로 변환
        content = response.choices[0].message.content
        # 가끔 GPT가 ```json ... ``` 이런 걸 붙일 때가 있어서 제거
        content = content.replace("```json", "").replace("```", "").strip()

        hints = json.loads(content)
        return {"found": True, "hints": hints}

    except Exception as e:
        print(f"에러 발생: {e}")
        return {
            "found": False,
            "msg": f"앗, 소크라테스 선생님이 잠시 자리를 비웠네요. (GPT 오류: {str(e)})"
        }


if __name__ == "__main__":
    import uvicorn

    # 로컬 테스트용 (Render에서는 필요 없지만 둠)
    uvicorn.run(app, host="127.0.0.1", port=8000)
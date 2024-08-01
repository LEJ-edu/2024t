import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyAd_MdoezucSMvvAv-BFL2XzxqtTsyQ3EQ" 

# few-shot 프롬프트 구성 함수 수정
def generate_personality_test(api_key, color):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 256,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    )
    prompt = f"""
    학생이 입력한 내용을 바탕으로 재미있는 성격 테스트 결과를 만들어줘. 
    단, 과학적 근거 없이 재미로 만든 테스트라는 점을 명시해줘.

    선택한 색깔: {color}

    성격 테스트 결과:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("색깔로 알아보는 성격 테스트")

# 사용자 입력 받기
color = st.selectbox("가장 좋아하는 색깔을 선택하세요.", ["빨강", "노랑", "파랑", "연두"])

if st.button("결과 보기"):
    # API 키로 성격 테스트 결과 생성 시도
    personality_test = generate_personality_test(api_key, color)

    # 결과 출력
    if personality_test is not None:
        st.markdown(to_markdown(personality_test))
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.") 
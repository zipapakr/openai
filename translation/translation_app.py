# OpenAI 패키지를 가져옵니다.
from openai import OpenAI
from dotenv import load_dotenv  # 환경 변수를 로드하는 dotenv 라이브러리의 load_dotenv 함수를 임포트합니다.
import os                      # 환경 변수에 접근하기 위해 os 모듈을 임포트합니다.

'''
Translate natural language text.
Prompt
SYSTEM : 
You will be provided with a sentence in English, and your task is to translate it into Korean.
USER : 
My name is Jane. What is yours?
'''

# OpenAI 클래스의 인스턴스를 생성합니다.
client = OpenAI(
    api_key=os.environ.get("API_KEY")  # "API_KEY"라는 이름으로 저장된 환경 변수에서 API 키를 가져옵니다.
)

# OpenAI API의 chat.completions.create 메서드를 호출하여 응답을 생성합니다.
response = client.chat.completions.create(
  model="gpt-3.5-turbo",  # 사용할 모델로 gpt-4를 지정합니다.
  messages=[
    {
      "role": "system",  # 시스템 역할로 모델에게 작업 지시를 제공합니다.
      "content": "You will be provided with a sentence in English, and your task is to translate it into Korean."
    },
    {
      "role": "user",  # 사용자 역할로 모델에게 번역할 문장을 제공합니다.
      "content": "My name is Jane. What is yours?"
    }
  ],
  temperature=0.7,  # 생성된 텍스트의 창의성 수준을 조정하는 온도 매개변수입니다. 값이 높을수록 더 창의적이고 예측 불가능한 텍스트를 생성합니다.
  max_tokens=64,  # 생성될 응답의 최대 토큰 수를 지정합니다.
  top_p=1  # 생성된 텍스트의 다양성을 조정하는 매개변수입니다. 값이 1이면 다양한 응답을 생성할 가능성이 높습니다.
)

print(response.choices[0].message.content)  # 생성된 챗봇 응답을 출력합니다.

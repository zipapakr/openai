from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 번역을 담당하는 Translator 클래스 정의
class Translator:
    def __init__(self):
        # OpenAI API 클라이언트를 초기화합니다.
        self.client = OpenAI(
            api_key=os.environ.get("API_KEY")  # 환경 변수에서 API 키를 가져옵니다.
        )

    # 영어 문장을 받아 한국어로 번역하는 메서드
    def translate_to_korean(self, english_sentence):
        # OpenAI API를 호출하여 번역을 수행합니다.
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # 사용할 모델로 gpt-3.5-turbo를 지정합니다.
            #response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",  # 시스템 역할로 모델에게 작업 지시를 제공합니다.
                    "content": "You will be provided with a sentence in English, and your task is to translate it into Korean."
                },
                {
                    "role": "user",  # 사용자 역할로 모델에게 번역할 문장을 제공합니다.
                    "content": english_sentence  # 입력받은 영어 문장을 설정합니다.
                }
            ],
            temperature=0.7,  # 생성된 텍스트의 창의성 수준을 조정하는 온도 매개변수입니다. 값이 높을수록 더 창의적이고 예측 불가능한 텍스트를 생성합니다.
            max_tokens=64,  # 생성될 응답의 최대 토큰 수를 지정합니다.
            top_p=1  # 생성된 텍스트의 다양성을 조정하는 매개변수입니다. 값이 1이면 다양한 응답을 생성할 가능성이 높습니다.
        )
        # 번역된 한국어 문장을 반환합니다.
        return response.choices[0].message.content

# 메인 함수 정의
def main():
    # Translator 클래스의 인스턴스를 생성합니다.
    translator = Translator()
    # 사용자로부터 영어 문장을 입력받습니다.
    english_sentence = input("Please enter a sentence in English: ")
    # 입력받은 영어 문장을 한국어로 번역합니다.
    translated_sentence = translator.translate_to_korean(english_sentence)
    # 번역된 한국어 문장을 출력합니다.
    print(f"Translated to Korean: {translated_sentence}")
    

# 이 스크립트가 직접 실행될 때 main 함수를 호출합니다.
if __name__ == "__main__":
    main()

# https://qiita.com/yamii/items/914fcae6599a4ac9f9fd
import openai
openai.api_key = "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"

# 設定プロンプト

def chat(text:str) -> str:
    """
    文字起こしした音声をchatGPTに渡して、レスポンスを取得する
    """
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {'role': 'system',
                          'content': "あなたの名前はファービーです。"},
                    {'role': 'user',
                      'content': text}
                    ],
                    temperature=0.0,)
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']
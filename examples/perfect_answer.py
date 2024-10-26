from flexi_prompt import FlexiPrompt
from openai import OpenAI
from anthropic import Anthropic
from google.colab import userdata
import os
import re

# Настройка API ключей и клиентов
os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = userdata.get("ANTHROPIC_API_KEY_TEST1")
openai = OpenAI()
anthropic = Anthropic()


def get_openai_answer(question, openai):
    openai_compleion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],

    )
    return openai_compleion.choices[0].message.content

def get_anthropic_answer(question, anthropic):
    message = anthropic.messages.create(
        max_tokens=4096,
        temperature=0,
        model="claude-3-haiku-20240307",
        system="You are a helpful assistant.",
        messages=[{"role": "user", "content": [{"type": "text", "text": question}]}],
    )
    return message.content[0].text

def get_answer_rate(rate_prompt, openai, anthropic):

  rates = []

  rate_raw = get_openai_answer(rate_prompt, openai)
  match = re.search(r"[1-9]", rate_raw)
  rates.append(int(match.group()) if match else 1)

  rate_raw = get_anthropic_answer(rate_prompt, anthropic)
  match = re.search(r"[1-9]", rate_raw)
  rates.append(int(match.group()) if match else 1)

  return sum(rates) / len(rates)

fp = FlexiPrompt()

# Настройка промптов
fp.question = input("enter your question")
fp.rate_prompt = """
Rate the answer to the question from 1 to 9, where 1 is the worst answer.
Be rigorous in your evaluation. Give back only one number as your answer.

Question:
 $question
Answer:
 $answer
"""

# Основной цикл
MAX_ATTEMPTS = 3
THRESHOLD_SCORE = 9
best_rate = 0
best_answer = ""

for attempt in range(MAX_ATTEMPTS):

    fp.answer = get_openai_answer(fp.question().build(), openai)
    answer_rate = get_answer_rate(fp.rate_prompt().build(), openai, anthropic)

    if answer_rate > best_rate:
        best_rate = answer_rate
        best_answer = fp.answer

    fp.answer = get_anthropic_answer(fp.question().build(), anthropic)
    answer_rate = get_answer_rate(fp.rate_prompt().build(), openai, anthropic)

    if answer_rate > best_rate:
        best_rate = answer_rate
        best_answer = fp.answer

    if best_rate >= THRESHOLD_SCORE:
        break

print(best_answer)
print("The answer rate is:", best_rate)

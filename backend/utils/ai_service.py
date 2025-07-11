import os
import json
import logging
from datetime import datetime
from openai import OpenAI

class AIService:
    def __init__(self):
        # 初始化OpenAI客户端
        try:
            api_key = os.environ.get("TONGYI_API_KEY")
            api_url = os.environ.get("TONGYI_API_URL")

            if not api_key or not api_url:
                logging.warning("TONGYI_API_KEY or TONGYI_API_URL is not set")
                self.client = None
            else:
                self.client = OpenAI(
                    api_key=api_key,
                    api_url=api_url
                )
        except Exception as e:
            logging.error(f"初始化AI服务失败: {str(e)}")
            self.client = None

    def get_analysis(self, subject, content):
        """
        获取当前题目的建议

        Args:
            subject: 题目
            content: 回答内容

        返回:
            成功:
                respond: {
                    message: 获取成功
                    analysis: 建议内容
                }
            失败:
                error: 错误信息   
        """
        try:
            if not self.client:
                return False
            
            # 构建提示词
            system_prompt = f"""你是一名青少年编程教育老师，此时用户在回答编程问题时遇到了困难，你的任务是结合用户的回答和题目，为用户提供下一步建议
                        请严格按照以下步骤形成回答：
                        1. 首先仔细分析题目与用户回答，这一部分不需要输出
                        2. 判断用户的回答是否正确：is_right = True/False
                        3. 如果回答正确，对用户答案的逻辑进行分析：analysis = "..."
                        4. 如果回答错误，对用户答案进行分析建议，循循善诱进行指导，注意不要直接给出答案：analalysis = "..."

                        回答格式：
                        {
                            "is_right": true/false,
                            "analysis": "..."
                        }

                        注意，请用适合8-14岁青少年的语言回答，提供足够的指导、解释，让用户能够理解。严格按照回答格式给出json格式的回答，analysis部分使用markdown格式。"""
            
            user_prompt = f"""
                        题目：{subject}
                        用户答案：{content}
                        """
            
            completion = openai.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5,
                max_tokens=1024,
            )

            respond = completion.choices[0].message.content.strip()

            return respond
        
        except Exception as e:
            logging.error(f"AI服务调用错误: {str(e)}")
            return False
        
    def ai_judge(self, subject, content):
        """
        
        """

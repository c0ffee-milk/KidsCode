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
            system_prompt = f"""你是一名专业的青少年编程教育老师。用户在解答编程题时遇到了困难，你的任务是结合题目和用户的回答，为用户提供下一步建议。
                        请严格按照以下步骤进行：
                        1. 仔细分析题目和用户的回答（这部分无需输出）。
                        2. 判断用户的回答是否正确，并用 is_right 字段表示，值为 True 或 False。
                        3. 如果回答正确，请对用户的解题思路和逻辑进行简要分析和鼓励，填写在 analysis 字段。
                        4. 如果回答错误，请分析用户的解题思路，指出存在的问题，并给予循序渐进的指导和建议，但不要直接给出正确答案，填写在 analysis 字段。

                        输出格式：
                        {
                            "is_right": True/False,
                            "analysis": "..." // 用适合8-14岁青少年的语言，内容支持markdown格式
                        }

                        注意事项：
                        1. 只输出上述 JSON 格式内容，不要输出多余内容。
                        2. analysis 字段请用通俗易懂、鼓励性强的语言，帮助用户理解和进步，内容可使用 markdown 格式。
                        """
            
            user_prompt = f"""
                            题目：{subject}
                            用户答案：{content}
                        """
            
            completion = OpenAI.client.chat.completions.create(
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
        ai判定

        Args:
            subject: 题目
            content: 回答

        返回:
            成功:
                message: success
                is_right: True/False
            失败:
                error: 错误信息
        """
        try:
            if not self.client:
                return False
            
            # 构建提示词
            system_prompt = f"""
                                你是一名专业的少儿编程教育老师。你的任务是根据题目内容，判断用户的回答是否正确。请你根据用户的回答进行推理，确认其答案是否能够完成题目要求。
                                输出要求：
                                1. 只返回 True 或 False，True 表示用户回答正确，False 表示用户回答错误。
                                2. 不要输出任何多余的字符或解释说明。
                            """
            
            user_prompt = f"""
                            题目：{subject}
                            用户答案：{content}
                        """
            
            completion = OpenAI.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        
        except Exception as e:
            logging.error(f"AI服务调用错误: {str(e)}")
            return False
        
    def ai_translate(self, subject, content):
        """
        将用户的内容翻译为行动指令

        Args:
            subject: 题目
            content: 回答内容

        返回:
            成功:
                respond: {
                    message: 获取成功
                    movement: 行动指令
                }
            失败:
                error: 错误信息   
        """
        try:
            if not self.client:
                return False
            
            # 构建提示词
            system_prompt = f"""
                                你是一名专业的少儿编程教育老师。你的任务是将用户输入的自然语言描述的逻辑，准确翻译为一串行动指令。
                                目前支持的指令如下：
                                1. 向左前进一个单位（用数字1表示）
                                2. 向右前进一个单位（用数字2表示）
                                3. 向上前进一个单位（用数字3表示）
                                4. 向下前进一个单位（用数字4表示）
                                5. 无限循环（用数字5表示，括号内为需要循环的动作序列，例如：无限重复向左和向右为5(12)）
                                请注意：
                                1. 用户输入中可能包含循环、跳转、判断等逻辑。请根据题目和用户输入，逐步推理每一步的行动。
                                2. 忽略地图的边界和障碍物（即使右边是障碍物，也可以输出向右的动作指令）。
                                3. 只需输出行动指令序列，不要输出多余内容。
                                请将用户输入的逻辑转换为如下 JSON 格式：
                                {
                                    "movement": "..."  // 由1、2、3、4、5组成的数字序列
                                }
                            """
            
            user_prompt = f"""
                            题目：{subject}
                            用户答案：{content}
                        """
            completion = OpenAI.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        
        except Exception as e:
            logging.error(f"AI服务调用错误: {str(e)}")
            return False
        
    def ai_evaluate(self, info):
        """
        根据用户的做题记录与评价，给出综合评估

        Args:
            info: 做题记录

        返回:
            成功:
                respond: {
                    message: 获取成功,
                    score: {
                        "逻辑思维": score1,
                        "创造力": score2,
                        "问题解决": score3,
                        "代码规范": score4,
                        "空间想象": score5
                    },
                    comment: 总体评价
                }
            失败:
                error: 错误信息   
        """
        try:
            if not self.client:
                return False
            
            # 构建提示词
            system_prompt = f"""
                                你是一名专业的少儿编程教育老师。请根据用户的做题记录和系统评价，从以下五个维度为用户进行评分，并给出每个维度1-100分的分数:逻辑思维、创造力、问题解决、代码规范、空间想象
                                最后，请根据整体表现，给出一段简明、具体的总体评价与提升建议。
                                请严格按照以下 JSON 格式输出：
                                {
                                    "score": {
                                        "逻辑思维": score1,
                                        "创造力": score2,
                                        "问题解决": score3,
                                        "代码规范": score4,
                                        "空间想象": score5
                                    },
                                    "comment": 总体评价与建议
                                }
                                注意：
                                1. 只输出JSON，不要输出多余内容
                                2. 评价要结合用户的实际做题表现，既要肯定优点，也要指出具体可提升的方向。
                            """
        
            user_prompt = f"""
                        做题记录{info}
                        """
            completion = OpenAI.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        
        except Exception as e:
            logging.error(f"AI服务调用错误: {str(e)}")
            return False

    def ai_comment(self, subject, content):
        """
        根据题目和用户输入，给出评价

        Args:
            subject: 题目
            content: 用户输入

        返回:
            成功:
                respond: {
                    message: 获取成功,
                    comment: 评价
                }
            失败:
                error: 错误信息   
        """
        try:
            if not self.client:
                return False
            
            # 构建提示词
            system_prompt = f"""
                                你是一名专业的少儿编程教育老师。你的任务是根据题目和用户的作答内容，给出针对性的评价和建议。

                                请注意：
                                - 评价要结合题目要求和用户的实际回答，既要肯定优点，也要指出可以改进的地方。
                                - 评价内容要简明、具体，适合8-14岁青少年理解，语言要鼓励、积极，帮助他们提升编程能力。
                                - 如有需要，可适当给出学习建议，但不要直接给出标准答案。
                                - 只输出评价内容，不要输出多余的解释或格式。
                                - 只用一段话评价，不超过150字，纯文本格式
                                严格按照以下JSON格式输出：
                                {
                                    "comment": "..."  // 以纯文本格式输出
                                }
                            """
        
            user_prompt = f"""
                            题目：{subject}
                            用户答案：{content}
                        """
            completion = OpenAI.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        
        except Exception as e:
            logging.error(f"AI服务调用错误: {str(e)}")
            return False
            



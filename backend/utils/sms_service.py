import random
import string
from datetime import datetime, timedelta
# from your_app import VerificationCode, db
import requests
import ssl

host = 'https://dfsns.market.alicloudapi.com'
path = '/data/send_sms'
method = 'POST'
appcode = 'a14cc6fe35ab4d26a97bd56477847115'
querys = ''
url = host + path

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

def send_sms(phone, code):
    bodys = {}
    bodys['content'] = f'code:{code}'
    bodys['template_id'] = 'CST_ptdie100'
    bodys['phone_number'] = phone
    headers = {
        'Authorization': 'APPCODE ' + appcode,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        response = requests.post(url, data=bodys, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        content = response.text
        print(content)
        return True
    except requests.RequestException as e:
        print(f"发送短信失败: {e}")
        return False

def save_verification_code(phone, code):
    expiration = datetime.now() + timedelta(minutes=5)
    existing = VerificationCode.query.filter_by(phone=phone).first()
    if existing:
        existing.code = code
        existing.expires_at = expiration
    else:
        new_code = VerificationCode(phone=phone, code=code, expires_at=expiration)
        db.session.add(new_code)
    db.session.commit()

def verify_code(phone, input_code):
    record = VerificationCode.query.filter_by(phone=phone).first()
    if not record:
        return False
    if record.expires_at < datetime.now():
        return False
    if record.code == input_code:
        return True
    return False

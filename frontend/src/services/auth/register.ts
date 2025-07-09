export const register = async (username: string, phone: string, password: string, code: string) => {
  const response = await fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ username, phone, password, code })
  });

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || '注册失败')
  }
  
  return await response.json()
};

export const sendCode = async (phone: string) => {
  const response = await fetch('http://localhost:5000/api/send-code', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ phone })
  });

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || '发送验证码失败')
  }
};

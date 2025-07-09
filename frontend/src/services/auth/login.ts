export const login = async (username: string, password: string) => {
  const response = await fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || '登录失败')
  }
  return await response.json();
};

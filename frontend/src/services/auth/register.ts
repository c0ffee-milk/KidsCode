export const register = async (username: string, password: string) => {
  const response = await fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) throw new Error('注册失败');
};

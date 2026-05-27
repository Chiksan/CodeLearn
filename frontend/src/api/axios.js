import axios from 'axios'

const api = axios.create({
  baseURL: '',
})

api.interceptors.request.use(config => {
  const storage = JSON.parse(localStorage.getItem('auth-storage') || '{}')
  const token = storage?.state?.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// При 401 — очищаем токен и редиректим на логин
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      const storage = JSON.parse(localStorage.getItem('auth-storage') || '{}')
      if (storage?.state?.token) {
        storage.state.token = null
        storage.state.user = null
        localStorage.setItem('auth-storage', JSON.stringify(storage))
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export default api

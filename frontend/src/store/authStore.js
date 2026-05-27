import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../api/axios'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      user: null,

      login: async (email, password) => {
        const form = new FormData()
        form.append('username', email)
        form.append('password', password)
        const { data } = await api.post('/api/auth/login', form)
        set({ token: data.access_token })
        // загружаем профиль
        const me = await api.get('/api/auth/me', {
          headers: { Authorization: `Bearer ${data.access_token}` }
        })
        set({ user: me.data })
        return data
      },

      register: async (email, username, password) => {
        const { data } = await api.post('/api/auth/register', { email, username, password })
        set({ user: data })
        return data
      },

      logout: () => set({ token: null, user: null }),
    }),
    { name: 'auth-storage' }
  )
)

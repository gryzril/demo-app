import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { User } from '@/api/entities/User';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
  }),
  actions: {
    setUser(user: User) {
      this.user = user;
    },
    clearUser() {
      this.user = null;
    },
  },
});
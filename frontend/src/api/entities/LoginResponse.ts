import type { User } from '../entities/User';

export interface LoginResponse {
  access_token: string;   // JWT
  tokenType: 'Bearer';
  expiresAt: number;     // epoch ms
  user: User;
}
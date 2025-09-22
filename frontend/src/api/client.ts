import type { LoginResponse } from "./entities/LoginResponse";
import { type User } from "./entities/User"

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://backend:8000").replace(/\/+$/,"");
const ACCESS_KEY = "access_token";

/* Auth Handling Helper Methods */

export const getAccessToken = () => localStorage.getItem(ACCESS_KEY);

export function setAccessToken(token: string | null) {
  if (token) localStorage.setItem(ACCESS_KEY, token);
  else localStorage.removeItem(ACCESS_KEY);
}

/* API Helper Methods */

export function joinUrl(path: string): string {
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}

export function jsonHeaders(init?: RequestInit): HeadersInit {
  return {
    "Content-Type": "application/json",
    ...(init?.headers || {}),
  };
}


/* API Methods */

export async function login(email: string, password: string): Promise<LoginResponse> {
  const payload = ({ email, password });
  
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: jsonHeaders(),
    credentials: "include",
    body: JSON.stringify(payload)
  })

  // Throw error based on response in-method
  if (!response.ok) throw new Error(await response.text());

  const data = (await response.json()) as LoginResponse;

  // If we get a good response, set user's access token
  setAccessToken(data.access_token);
  return data;
}

export async function refreshToken(): Promise<string | null> {
  try {
    const response = await fetch(`${BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) return null;

    const data = (await response.json()) as { access_token?: string };
    if (data?.access_token) {
      setAccessToken(data.access_token);
      return data.access_token;
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * 
 * @param token JTW Auth Token
 * @returns Fetch /me results
 */
export function fetchMe(token?: string): Promise<Response> {
  const headers: HeadersInit = token ? { Authorization: `Bearer ${token}` } : {};
  return fetch(`${BASE_URL}/me`, { credentials: "include", headers });
}

/**
 * Get User Information. If initial fetch fails, refresh token
 * @returns User Object
 */
export async function me(): Promise<User> {
  const currentCreds = await fetchMe(getAccessToken() ?? undefined)

  if (currentCreds.ok) {
    return (await currentCreds.json()) as User;
  }

  const refreshedToken = await refreshToken();

  if (!refreshedToken) {
    throw Error("Failed to refresh auth token")
  }

  const retry = await fetchMe(refreshedToken);

  if (!retry.ok) {
    throw Error("Failed to fetch user with refreshed auth token")
  }

  return (await retry.json()) as User

}
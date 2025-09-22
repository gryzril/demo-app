import { type Task, type TaskCreate, type TaskUpdate, type Status } from './entities/Tasks'
import { jsonHeaders } from "./client"

const BASE = (import.meta as any)?.env?.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

export async function getAllTasks(): Promise<Task[]> {
  const r = await fetch(`${BASE}/tasks`, {
    method: 'GET',
    headers: jsonHeaders(),
    credentials: 'include',
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getTask(id: number): Promise<Task> {
  const r = await fetch(`${BASE}/tasks/${id}`, {
    method: 'GET',
    headers: jsonHeaders(),
    credentials: 'include',
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createTask(body: TaskCreate): Promise<Task> {
  const r = await fetch(`${BASE}/tasks`, {
    method: 'POST',
    headers: jsonHeaders(),
    credentials: 'include',
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function updateTask(id: number, patch: TaskUpdate): Promise<Task> {
  const r = await fetch(`${BASE}/tasks/${id}`, {
    method: 'PATCH',
    headers: jsonHeaders(),
    credentials: 'include',
    body: JSON.stringify(patch),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function deleteTask(id: number): Promise<void> {
  const r = await fetch(`${BASE}/tasks/${id}`, {
    method: 'DELETE',
    headers: jsonHeaders(),
    credentials: 'include',
  });
  if (!r.ok) throw new Error(await r.text());
}
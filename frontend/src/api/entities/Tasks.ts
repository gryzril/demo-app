export type Status = 'todo' | 'in_progress' | 'done';

export interface Label {
  id: number;
  name: string;
  color?: string | null;
}

export interface Task {
  id: number;
  userId: number;
  title: string;
  description?: string | null;
  status: Status;
  due_date?: string | null;      // ISO
  labels: Label[];
  createdAt?: string;
  updatedAt?: string;
}

export interface TaskCreate {
  title: string;
  description?: string | null;
  status: Status;
  due_date?: string | null;      // ISO
  label_ids?: number[];
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  status?: Status;
  due_date?: string | null;      // ISO
  label_ids?: number[];
}
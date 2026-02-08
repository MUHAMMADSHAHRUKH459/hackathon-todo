// lib/api.ts
const API_URL = 'http://127.0.0.1:8000';

interface LoginData {
  username: string;
  password: string;
}

interface RegisterData extends LoginData {
  email: string;
}

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: string;  // NEW - Phase 5
  due_date: string | null;  // NEW - Phase 5
  user_id: number;
  created_at: string;
  updated_at: string;
}

// Auth API
export const api = {
  // Register
  async register(data: RegisterData) {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Login
  async login(data: LoginData) {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Invalid credentials');
    return res.json();
  },

  // Get tasks
  async getTasks(token: string): Promise<Task[]> {
    const res = await fetch(`${API_URL}/api/tasks`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },

  // Create task (Updated - Phase 5)
  async createTask(token: string, data: { title: string; description: string; priority?: string; due_date?: string }) {
    const res = await fetch(`${API_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create task');
    return res.json();
  },

  // Update task
  async updateTask(token: string, id: number, data: Partial<Task>) {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update task');
    return res.json();
  },

  // Delete task
  async deleteTask(token: string, id: number) {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to delete task');
    return res.json();
  },
};
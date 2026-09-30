import { create } from 'zustand';
import api from './api';

export interface Model {
  id: string;
  name: string;
  description: string;
  source_type: string;
  format?: string;
  status: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  model_id: string;
  role: string;
  system_prompt: string;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  nodes: any[];
  edges: any[];
}

interface AppState {
  models: Model[];
  agents: Agent[];
  workflows: Workflow[];
  fetchModels: () => Promise<void>;
  fetchAgents: () => Promise<void>;
  fetchWorkflows: () => Promise<void>;
  createModel: (data: any) => Promise<void>;
  createAgent: (data: any) => Promise<void>;
  createWorkflow: (data: any) => Promise<void>;
}

export const useStore = create<AppState>((set) => ({
  models: [],
  agents: [],
  workflows: [],
  
  fetchModels: async () => {
    const res = await api.get('/models/');
    set({ models: res.data });
  },
  
  fetchAgents: async () => {
    const res = await api.get('/agents/');
    set({ agents: res.data });
  },
  
  fetchWorkflows: async () => {
    const res = await api.get('/workflows/');
    set({ workflows: res.data });
  },
  
  createModel: async (data: any) => {
    await api.post('/models/', data);
    const res = await api.get('/models/');
    set({ models: res.data });
  },
  
  createAgent: async (data: any) => {
    await api.post('/agents/', data);
    const res = await api.get('/agents/');
    set({ agents: res.data });
  },
  
  createWorkflow: async (data: any) => {
    await api.post('/workflows/', data);
    const res = await api.get('/workflows/');
    set({ workflows: res.data });
  }
}));

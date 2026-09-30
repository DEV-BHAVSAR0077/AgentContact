import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { LayoutDashboard, Box, Network, Cpu } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Models from './pages/Models';
import Agents from './pages/Agents';
import WorkflowBuilder from './pages/WorkflowBuilder';
import Workflows from './pages/Workflows';

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-50">
      <div className="w-64 bg-white border-r border-slate-200 p-4">
        <h1 className="text-xl font-bold text-slate-800 mb-8 flex items-center">
          <Network className="mr-2" />
          AgentFlow
        </h1>
        <nav className="space-y-2">
          <Link to="/" className="flex items-center p-2 text-slate-700 hover:bg-slate-100 rounded">
            <LayoutDashboard className="mr-3 h-5 w-5" /> Dashboard
          </Link>
          <Link to="/models" className="flex items-center p-2 text-slate-700 hover:bg-slate-100 rounded">
            <Box className="mr-3 h-5 w-5" /> Models
          </Link>
          <Link to="/agents" className="flex items-center p-2 text-slate-700 hover:bg-slate-100 rounded">
            <Cpu className="mr-3 h-5 w-5" /> Agents
          </Link>
          <Link to="/workflows" className="flex items-center p-2 text-slate-700 hover:bg-slate-100 rounded">
            <Network className="mr-3 h-5 w-5" /> Workflows
          </Link>
        </nav>
      </div>
      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/models" element={<Models />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/workflows" element={<Workflows />} />
          <Route path="/workflows/:id" element={<WorkflowBuilder />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;

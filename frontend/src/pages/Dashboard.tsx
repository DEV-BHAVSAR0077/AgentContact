import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState({ models: 0, agents: 0, workflows: 0 });

  useEffect(() => {
    // Fetch stats in a real app
    setStats({ models: 2, agents: 3, workflows: 1 });
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h2 className="text-slate-500 text-sm font-medium">Total Models</h2>
          <p className="text-3xl font-bold text-slate-800">{stats.models}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h2 className="text-slate-500 text-sm font-medium">Total Agents</h2>
          <p className="text-3xl font-bold text-slate-800">{stats.agents}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h2 className="text-slate-500 text-sm font-medium">Active Workflows</h2>
          <p className="text-3xl font-bold text-slate-800">{stats.workflows}</p>
        </div>
      </div>
    </div>
  );
}

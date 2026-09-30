import { useEffect } from 'react';
import { useStore } from '../store';
import { Network, Plus } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

export default function Workflows() {
  const { workflows, fetchWorkflows } = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    fetchWorkflows();
  }, [fetchWorkflows]);

  const handleCreate = async () => {
    try {
      const res = await api.post('/workflows/', {
        name: 'New Workflow',
        description: 'Auto-generated workflow',
        nodes: [],
        edges: []
      });
      navigate(`/workflows/${res.data.id}`);
    } catch (e) {
      console.error(e);
      alert('Failed to create workflow');
    }
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Workflows</h1>
        <button onClick={handleCreate} className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium transition-colors">
          <Plus className="w-4 h-4 mr-2" /> New Workflow
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {workflows.map(wf => (
          <div key={wf.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-5 border-b border-slate-100">
              <h3 className="text-lg font-bold text-slate-800 mb-1">{wf.name}</h3>
              <p className="text-sm text-slate-500">{wf.description}</p>
            </div>
            <div className="px-5 py-3 bg-slate-50 flex justify-end space-x-2">
              <Link to={`/workflows/${wf.id}`} className="text-sm text-indigo-600 font-medium hover:text-indigo-700 transition-colors">Edit in Builder</Link>
            </div>
          </div>
        ))}
        {workflows.length === 0 && (
          <div className="col-span-full py-10 text-center text-slate-500 bg-white border border-dashed rounded-lg">
            No workflows yet. Create one!
          </div>
        )}
      </div>
    </div>
  );
}

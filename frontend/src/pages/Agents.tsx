import { useEffect } from 'react';
import { Cpu, Plus } from 'lucide-react';
import { useStore } from '../store';
import api from '../api';

export default function Agents() {
  const { agents, fetchAgents, models, fetchModels } = useStore();

  useEffect(() => {
    fetchAgents();
    fetchModels();
  }, [fetchAgents, fetchModels]);

  const handleAdd = async () => {
    const name = prompt("Enter agent name:");
    if (!name) return;
    try {
      await api.post('/agents/', {
        name,
        description: "New agent added from UI",
        role: "assistant",
        system_prompt: "You are a helpful assistant.",
        model_id: models.length > 0 ? models[0].id : null
      });
      fetchAgents();
    } catch (e) {
      alert("Failed to add agent");
    }
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Agents Library</h1>
        <button onClick={handleAdd} className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium transition-colors">
          <Plus className="w-4 h-4 mr-2" /> Add Agent
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map(agent => (
          <div key={agent.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-5 border-b border-slate-100">
              <div className="flex justify-between items-start mb-3">
                <div className="flex items-center text-blue-600 bg-blue-50 px-2 py-1 rounded text-xs font-semibold">
                  <Cpu className="w-3 h-3 mr-1" /> {agent.role.toUpperCase()}
                </div>
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-1">{agent.name}</h3>
              <p className="text-sm text-slate-500 line-clamp-2">{agent.description}</p>
            </div>
          </div>
        ))}
        {agents.length === 0 && (
          <div className="col-span-full py-10 text-center text-slate-500 border border-dashed rounded-lg">
            No agents found.
          </div>
        )}
      </div>
    </div>
  );
}

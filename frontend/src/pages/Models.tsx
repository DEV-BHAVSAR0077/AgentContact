import { useEffect } from 'react';
import { Box, Plus } from 'lucide-react';
import { useStore } from '../store';
import api from '../api';

export default function Models() {
  const { models, fetchModels } = useStore();

  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  const handleAdd = async () => {
    const name = prompt("Enter model name:");
    if (!name) return;
    try {
      await api.post('/models/', {
        name,
        description: "Added from UI",
        source_type: "api"
      });
      fetchModels();
    } catch (e) {
      alert("Failed to add model");
    }
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Models Library</h1>
        <button onClick={handleAdd} className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium transition-colors">
          <Plus className="w-4 h-4 mr-2" /> Add Model
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models.map(model => (
          <div key={model.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-5 border-b border-slate-100">
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center text-indigo-600 bg-indigo-50 px-2 py-1 rounded text-xs font-semibold">
                  <Box className="w-3 h-3 mr-1" /> {model.source_type.toUpperCase()}
                </div>
                <span className={`flex items-center text-xs font-semibold ${model.status === 'READY' ? 'text-green-600' : 'text-yellow-600'}`}>
                  <span className={`w-2 h-2 rounded-full ${model.status === 'READY' ? 'bg-green-500' : 'bg-yellow-500'} mr-1`}></span> {model.status}
                </span>
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-1">{model.name}</h3>
              <p className="text-sm text-slate-500">{model.description}</p>
              {model.format && <p className="text-xs text-slate-400 mt-2 font-mono">{model.format}</p>}
            </div>
          </div>
        ))}
        {models.length === 0 && (
          <div className="col-span-full py-10 text-center text-slate-500 border border-dashed rounded-lg">
            No models. Click Add Model.
          </div>
        )}
      </div>
    </div>
  );
}

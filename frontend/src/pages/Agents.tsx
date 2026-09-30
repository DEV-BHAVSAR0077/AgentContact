import { Cpu, Plus } from 'lucide-react';

export default function Agents() {
  const handleAdd = () => alert("Add Agent modal opening...");
  const handleEdit = () => alert("Edit Agent modal opening...");
  const handleUse = () => alert("Redirecting to Workflow Builder with agent selected...");

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Agents Library</h1>
        <button onClick={handleAdd} className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium transition-colors">
          <Plus className="w-4 h-4 mr-2" /> Add Agent
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Agent Card */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
          <div className="p-5 border-b border-slate-100">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center text-blue-600 bg-blue-50 px-2 py-1 rounded text-xs font-semibold">
                <Cpu className="w-3 h-3 mr-1" /> Autonomous Agent
              </div>
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">Research Agent</h3>
            <p className="text-sm text-slate-500 mb-4 line-clamp-2">Gathers information from provided datasets and summarizes findings intelligently.</p>
            <div className="text-xs text-slate-400 font-medium">Model: <span className="text-slate-600">Gemini Research Model</span></div>
          </div>
          <div className="px-5 py-3 bg-slate-50 flex justify-end space-x-2">
            <button onClick={handleEdit} className="text-sm text-slate-600 hover:text-indigo-600 font-medium transition-colors">Edit</button>
            <button onClick={handleUse} className="text-sm text-indigo-600 font-medium hover:text-indigo-700 transition-colors">Use in Workflow</button>
          </div>
        </div>
      </div>
    </div>
  );
}

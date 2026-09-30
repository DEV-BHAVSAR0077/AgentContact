import { Box, Plus } from 'lucide-react';

export default function Models() {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Models Library</h1>
        <button className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium">
          <Plus className="w-4 h-4 mr-2" /> Add Model
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* API Model Card */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
          <div className="p-5 border-b border-slate-100">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center text-indigo-600 bg-indigo-50 px-2 py-1 rounded text-xs font-semibold">
                <Box className="w-3 h-3 mr-1" /> API Model
              </div>
              <span className="flex items-center text-xs font-semibold text-green-600">
                <span className="w-2 h-2 rounded-full bg-green-500 mr-1"></span> READY
              </span>
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">Gemini Research Model</h3>
            <p className="text-sm text-slate-500">Google Gemini Pro 1.5</p>
          </div>
          <div className="px-5 py-3 bg-slate-50 flex justify-end space-x-2">
            <button className="text-sm text-slate-600 hover:text-indigo-600 font-medium">Edit</button>
            <button className="text-sm text-indigo-600 font-medium">Use in Workflow</button>
          </div>
        </div>

        {/* Uploaded Model Card */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
          <div className="p-5 border-b border-slate-100">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center text-emerald-600 bg-emerald-50 px-2 py-1 rounded text-xs font-semibold">
                <Box className="w-3 h-3 mr-1" /> Uploaded Model
              </div>
              <span className="flex items-center text-xs font-semibold text-green-600">
                <span className="w-2 h-2 rounded-full bg-green-500 mr-1"></span> READY
              </span>
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">Customer Churn Model</h3>
            <div className="flex items-center space-x-2 text-xs text-slate-500">
              <span>Scikit-Learn</span>
              <span>•</span>
              <span>.pkl</span>
              <span>•</span>
              <span>v1.2</span>
            </div>
          </div>
          <div className="px-5 py-3 bg-slate-50 flex justify-end space-x-2">
            <button className="text-sm text-slate-600 hover:text-indigo-600 font-medium">Edit</button>
            <button className="text-sm text-indigo-600 font-medium">Use in Workflow</button>
          </div>
        </div>
      </div>
    </div>
  );
}

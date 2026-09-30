import { Handle, Position } from '@xyflow/react';
import { Cpu } from 'lucide-react';

export default function AgentNode({ data, isConnectable }: any) {
  return (
    <div className="bg-white border-2 border-indigo-500 rounded-lg p-4 shadow-md w-64">
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} className="w-3 h-3 bg-indigo-500" />
      <div className="flex items-center mb-2">
        <Cpu className="text-indigo-500 mr-2 h-5 w-5" />
        <div className="font-bold text-sm text-slate-800">{data.label}</div>
      </div>
      <div className="text-xs text-slate-500">{data.modelName || 'No model attached'}</div>
      <div className="mt-2 text-xs font-semibold text-green-600 flex items-center">
        <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
        Ready
      </div>
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} className="w-3 h-3 bg-indigo-500" />
    </div>
  );
}

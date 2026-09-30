import { Handle, Position } from '@xyflow/react';
import { Box } from 'lucide-react';

export default function ModelNode({ data, isConnectable }: any) {
  return (
    <div className="bg-white border-2 border-emerald-500 rounded-lg p-4 shadow-md w-64">
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} className="w-3 h-3 bg-emerald-500" />
      <div className="flex items-center mb-2">
        <Box className="text-emerald-500 mr-2 h-5 w-5" />
        <div className="font-bold text-sm text-slate-800">{data.label}</div>
      </div>
      <div className="text-xs text-slate-500">{data.framework || 'API Model'}</div>
      <div className="mt-2 text-xs font-semibold text-green-600 flex items-center">
        <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
        Model Ready
      </div>
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} className="w-3 h-3 bg-emerald-500" />
    </div>
  );
}

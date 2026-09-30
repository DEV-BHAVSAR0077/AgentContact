import { useState, useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  type Connection,
  type Edge,
  ReactFlowProvider,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import AgentNode from '../components/nodes/AgentNode';
import ModelNode from '../components/nodes/ModelNode';
import { Play, Save, Plus } from 'lucide-react';

const nodeTypes = {
  agentNode: AgentNode,
  modelNode: ModelNode,
};

const initialNodes = [
  { id: '1', type: 'agentNode', position: { x: 250, y: 100 }, data: { label: 'Research Agent' } },
  { id: '2', type: 'modelNode', position: { x: 250, y: 300 }, data: { label: 'Churn Classifier', framework: 'Scikit-Learn' } },
];
const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];

let id = 3;
const getId = () => `${id++}`;

function Builder() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [executionLogs, setExecutionLogs] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const onConnect = useCallback((params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const addAgent = () => {
    const newNode = {
      id: getId(),
      type: 'agentNode',
      position: { x: 100, y: 100 },
      data: { label: 'New Agent' },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const addModel = () => {
    const newNode = {
      id: getId(),
      type: 'modelNode',
      position: { x: 300, y: 100 },
      data: { label: 'New Model', framework: 'API Model' },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const executeWorkflow = () => {
    setIsRunning(true);
    setExecutionLogs(["Workflow started..."]);
    
    // Simulate real-time execution logs
    let step = 0;
    const interval = setInterval(() => {
      if (step < nodes.length) {
        setExecutionLogs(prev => [...prev, `Executing node: ${nodes[step].data.label}`]);
        step++;
      } else {
        setExecutionLogs(prev => [...prev, "Workflow completed successfully."]);
        setIsRunning(false);
        clearInterval(interval);
      }
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="bg-white border-b border-slate-200 p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-slate-800">Workflow Builder</h1>
        <div className="flex space-x-2">
          <button onClick={addAgent} className="flex items-center px-3 py-2 bg-slate-100 text-slate-700 rounded hover:bg-slate-200 text-sm font-medium">
            <Plus className="w-4 h-4 mr-1" /> Agent
          </button>
          <button onClick={addModel} className="flex items-center px-3 py-2 bg-slate-100 text-slate-700 rounded hover:bg-slate-200 text-sm font-medium">
            <Plus className="w-4 h-4 mr-1" /> Model
          </button>
          <button className="flex items-center px-4 py-2 bg-indigo-50 text-indigo-700 rounded hover:bg-indigo-100 text-sm font-medium border border-indigo-200">
            <Save className="w-4 h-4 mr-2" /> Save Workflow
          </button>
          <button onClick={executeWorkflow} disabled={isRunning} className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm font-medium disabled:opacity-50">
            <Play className="w-4 h-4 mr-2" /> {isRunning ? 'Running...' : 'Run'}
          </button>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col lg:flex-row h-full">
        {/* Canvas area */}
        <div className="flex-1 h-full relative" style={{ minHeight: '500px' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
          >
            <Controls />
            <MiniMap />
            <Background gap={12} size={1} />
          </ReactFlow>
        </div>
        
        {/* Logs Panel */}
        <div className="w-full lg:w-80 border-t lg:border-t-0 lg:border-l border-slate-200 bg-slate-50 flex flex-col h-64 lg:h-full">
          <div className="p-3 border-b border-slate-200 bg-white font-semibold text-sm text-slate-700">
            Execution Logs
          </div>
          <div className="flex-1 p-4 overflow-auto font-mono text-xs text-slate-600 space-y-2">
            {executionLogs.map((log, index) => (
              <div key={index} className="border-b border-slate-100 pb-1">{log}</div>
            ))}
            {executionLogs.length === 0 && <div className="text-slate-400 italic">No execution logs yet. Click Run to start.</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function WorkflowBuilder() {
  return (
    <ReactFlowProvider>
      <Builder />
    </ReactFlowProvider>
  );
}

import { useState, useCallback, useRef, useEffect } from 'react';
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
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

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
    try {
      setIsRunning(true);
      setExecutionLogs(["Workflow started..."]);
      setChatMessages([{role: 'system', content: 'Workflow started. You can now chat with the agents.'}]);
      
      // Simulate real-time execution logs safely
      let step = 0;
      const interval = setInterval(() => {
        try {
          if (step < nodes.length) {
            const currentNode = nodes[step];
            const nodeName = currentNode?.data?.label || currentNode?.id || 'Unknown Node';
            setExecutionLogs(prev => [...prev, `Executing node: ${nodeName}`]);
            step++;
          } else {
            setExecutionLogs(prev => [...prev, "Workflow completed successfully."]);
            setIsRunning(false);
            clearInterval(interval);
          }
        } catch (intervalError) {
          console.error("Execution error:", intervalError);
          setExecutionLogs(prev => [...prev, `Error during execution: ${String(intervalError)}`]);
          setIsRunning(false);
          clearInterval(interval);
        }
      }, 1500);
    } catch (err) {
      console.error("Startup error:", err);
      setIsRunning(false);
      alert("Failed to start workflow execution.");
    }
  };

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;
    setChatMessages(prev => [...prev, {role: 'user', content: chatInput}]);
    setChatInput('');
    
    // Mock bot response
    setTimeout(() => {
      setChatMessages(prev => [...prev, {role: 'agent', content: 'I have processed your request based on the current workflow.'}]);
      setExecutionLogs(prev => [...prev, 'Agent responded to user input.']);
    }, 1000);
  };

  const saveWorkflow = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert('Workflow saved successfully!');
    }, 800);
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
          <button onClick={saveWorkflow} disabled={isSaving} className="flex items-center px-4 py-2 bg-indigo-50 text-indigo-700 rounded hover:bg-indigo-100 text-sm font-medium border border-indigo-200 disabled:opacity-50">
            <Save className="w-4 h-4 mr-2" /> {isSaving ? 'Saving...' : 'Save Workflow'}
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
        
        {/* Right Sidebar (Chat + Logs) */}
        <div className="w-full lg:w-96 border-t lg:border-t-0 lg:border-l border-slate-200 bg-slate-50 flex flex-col h-96 lg:h-full">
          
          {/* Chat Panel */}
          <div className="flex-1 flex flex-col border-b border-slate-200">
            <div className="p-3 border-b border-slate-200 bg-white font-semibold text-sm text-slate-700">
              Interactive Chat
            </div>
            <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-slate-50 min-h-[200px]">
              {chatMessages.length === 0 ? (
                <div className="text-slate-400 text-sm italic text-center mt-4">Run the workflow to start chatting.</div>
              ) : (
                chatMessages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-lg p-2 text-sm ${msg.role === 'user' ? 'bg-indigo-600 text-white' : msg.role === 'system' ? 'bg-slate-200 text-slate-600 italic' : 'bg-white border border-slate-200 text-slate-800'}`}>
                      {msg.content}
                    </div>
                  </div>
                ))
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="p-3 bg-white border-t border-slate-200 flex">
              <input 
                type="text" 
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type a message..."
                disabled={!isRunning && chatMessages.length === 0}
                className="flex-1 border border-slate-300 rounded-l px-3 py-2 text-sm focus:outline-none focus:border-indigo-500 disabled:bg-slate-100"
              />
              <button 
                onClick={handleSendMessage}
                disabled={!isRunning && chatMessages.length === 0}
                className="bg-indigo-600 text-white px-4 py-2 rounded-r text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </div>

          {/* Logs Panel */}
          <div className="h-1/3 flex flex-col min-h-[150px]">
            <div className="p-3 border-b border-slate-200 bg-white font-semibold text-sm text-slate-700 flex justify-between items-center">
              <span>Execution Logs</span>
              {isRunning && <span className="flex h-2 w-2 relative"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span></span>}
            </div>
            <div className="flex-1 p-3 overflow-y-auto font-mono text-xs text-slate-600 space-y-1.5 bg-slate-900 text-green-400">
              {executionLogs.map((log, index) => (
                <div key={index} className="pb-1">{'>'} {log}</div>
              ))}
              {executionLogs.length === 0 && <div className="text-slate-500 italic">No execution logs yet. Click Run to start.</div>}
            </div>
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

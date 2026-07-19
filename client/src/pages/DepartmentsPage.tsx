import React from 'react';
import { TrendingUp, Package, DollarSign, Truck, CheckCircle, Cpu } from 'lucide-react';

export const DepartmentsPage: React.FC = () => {
  const departments = [
    {
      id: 'sales',
      name: 'Sales Agent (Specialist)',
      icon: TrendingUp,
      accent: '#6366F1',
      confidence: 0.92,
      status: 'ACTIVE',
      toolMetrics: {
        'Q3 Sales Forecast': '25,000 units',
        'Projected Growth': '+12.5%',
        'CRM Pipeline Confidence': '92%',
      },
      agentReasoning: 'Recommends aggressive promotion in Western Region due to 12.5% demand increase.',
    },
    {
      id: 'inventory',
      name: 'Inventory Agent (Specialist)',
      icon: Package,
      accent: '#10B981',
      confidence: 0.89,
      status: 'ACTIVE',
      toolMetrics: {
        'Current Stock Level': '1,200 units',
        'Reorder Threshold': '500 units',
        'Stockout Risk': 'LOW',
      },
      agentReasoning: 'Requests safety stock buffer increase of 200 units to avoid stockouts during Q3 promo.',
    },
    {
      id: 'finance',
      name: 'Finance Agent (Specialist)',
      icon: DollarSign,
      accent: '#F59E0B',
      confidence: 0.95,
      status: 'ACTIVE',
      toolMetrics: {
        'Available Budget Cap': '$50,000 USD',
        'Burn Rate': 'NORMAL',
        'Approval Limit': '$100,000 USD',
      },
      agentReasoning: 'Approves up to $15,000 for promo spend provided freight expedition stays under $5,000.',
    },
    {
      id: 'logistics',
      name: 'Logistics Agent (Specialist)',
      icon: Truck,
      accent: '#06B6D4',
      confidence: 0.90,
      status: 'ACTIVE',
      toolMetrics: {
        'Carrier Capacity': '94%',
        'Average Lead Time': '3 Days',
        'Expedited Freight': 'AVAILABLE',
      },
      agentReasoning: 'Confirms carrier capacity for expedited freight within 3-day delivery window.',
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>Specialized Domain Agents</h2>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>Autonomous AI domain agents powered by Google ADK orchestrator</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        {departments.map((dept) => {
          const Icon = dept.icon;
          return (
            <div key={dept.id} className="glass-panel glass-card-interactive" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {/* Card Header */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{
                    width: '42px',
                    height: '42px',
                    borderRadius: '10px',
                    background: `rgba(${parseInt(dept.accent.slice(1,3),16)}, ${parseInt(dept.accent.slice(3,5),16)}, ${parseInt(dept.accent.slice(5,7),16)}, 0.15)`,
                    border: `1px solid ${dept.accent}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <Icon size={22} color={dept.accent} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF', margin: 0 }}>{dept.name}</h3>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Cpu size={12} color="#818CF8" /> ADK Specialist Model
                    </div>
                  </div>
                </div>

                <span style={{
                  fontSize: '11px',
                  fontWeight: 600,
                  padding: '4px 8px',
                  borderRadius: '999px',
                  background: 'rgba(16, 185, 129, 0.15)',
                  color: '#10B981',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}>
                  <CheckCircle size={12} /> {dept.status}
                </span>
              </div>

              {/* Tool Metrics Grid */}
              <div style={{
                background: 'rgba(0,0,0,0.2)',
                borderRadius: '8px',
                padding: '12px',
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '10px',
                border: '1px solid rgba(255,255,255,0.04)'
              }}>
                {Object.entries(dept.toolMetrics).map(([key, val]) => (
                  <div key={key}>
                    <div style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>{key}</div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#FFFFFF', marginTop: '2px' }}>{val}</div>
                  </div>
                ))}
              </div>

              {/* Reasoning */}
              <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4', background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '6px', borderLeft: `3px solid ${dept.accent}` }}>
                <span style={{ fontWeight: 600, color: '#FFFFFF' }}>Agent Consensus: </span>
                {dept.agentReasoning}
              </div>

              {/* Confidence Meter */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '11px' }}>
                <span style={{ color: 'var(--text-dim)' }}>Confidence Level</span>
                <span style={{ color: dept.accent, fontWeight: 700 }}>{(dept.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

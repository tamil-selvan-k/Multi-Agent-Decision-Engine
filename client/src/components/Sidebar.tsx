import React from 'react';
import { LayoutDashboard, Building2, BrainCircuit, CheckCircle2, SlidersHorizontal } from 'lucide-react';

export type TabType = 'dashboard' | 'departments' | 'decision' | 'approval' | 'simulation';

interface SidebarProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  pendingApprovalsCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, pendingApprovalsCount = 2 }) => {
  const menuItems = [
    { id: 'dashboard' as TabType, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'departments' as TabType, label: 'Departments', icon: Building2 },
    { id: 'decision' as TabType, label: 'Decision Engine', icon: BrainCircuit },
    { id: 'approval' as TabType, label: 'Approvals', icon: CheckCircle2, badge: pendingApprovalsCount },
    { id: 'simulation' as TabType, label: 'Simulation', icon: SlidersHorizontal },
  ];

  return (
    <aside style={{
      width: '230px',
      background: 'rgba(11, 15, 23, 0.95)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      padding: '16px 12px',
      gap: '6px'
    }}>
      <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-dim)', padding: '0 12px 8px', letterSpacing: '0.05em' }}>
        CORE PLATFORM
      </div>
      {menuItems.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '10px 14px',
              borderRadius: '8px',
              border: isActive ? '1px solid var(--border-highlight)' : '1px solid transparent',
              background: isActive ? 'linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%)' : 'transparent',
              color: isActive ? '#FFFFFF' : 'var(--text-muted)',
              cursor: 'pointer',
              fontWeight: isActive ? 600 : 400,
              fontSize: '13px',
              transition: 'all 0.15s ease'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Icon size={18} color={isActive ? '#818CF8' : '#9CA3AF'} />
              <span>{item.label}</span>
            </div>
            {item.badge ? (
              <span style={{
                background: '#F43F5E',
                color: '#FFFFFF',
                fontSize: '10px',
                fontWeight: 700,
                borderRadius: '999px',
                padding: '2px 6px',
              }}>
                {item.badge}
              </span>
            ) : null}
          </button>
        );
      })}
    </aside>
  );
};

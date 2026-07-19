import React from 'react';
import { Bot, LogOut, ShieldCheck, Zap } from 'lucide-react';
import type { User, Role } from '../types';

interface NavbarProps {
  user: User | null;
  onLogout: () => void;
  onSwitchRole: (role: Role) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ user, onLogout, onSwitchRole }) => {
  return (
    <header style={{
      height: '64px',
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(11, 15, 23, 0.85)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 50
    }}>
      {/* Brand & Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 16px rgba(99, 102, 241, 0.4)'
        }}>
          <Bot size={22} color="#FFFFFF" />
        </div>
        <div>
          <h1 style={{ fontSize: '16px', fontWeight: 700, margin: 0, color: '#FFFFFF', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '8px' }}>
            Multi-Agent Decision Engine
            <span style={{
              fontSize: '10px',
              padding: '2px 6px',
              borderRadius: '999px',
              background: 'rgba(16, 185, 129, 0.15)',
              color: '#10B981',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              fontWeight: 600
            }}>
              LIVE ADK
            </span>
          </h1>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', margin: 0 }}>Neuro-Symbolic Enterprise Orchestrator</p>
        </div>
      </div>

      {/* User Controls & Quick Role Switcher */}
      {user && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Quick Role Switcher for Demo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(255,255,255,0.04)', padding: '4px 8px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <Zap size={14} color="#F59E0B" />
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 500 }}>Demo Role:</span>
            {(['Admin', 'Manager', 'Analyst', 'Executive'] as Role[]).map((r) => (
              <button
                key={r}
                onClick={() => onSwitchRole(r)}
                style={{
                  fontSize: '11px',
                  padding: '3px 8px',
                  borderRadius: '6px',
                  border: user.role === r ? '1px solid #6366F1' : '1px solid transparent',
                  background: user.role === r ? 'rgba(99, 102, 241, 0.2)' : 'transparent',
                  color: user.role === r ? '#818CF8' : 'var(--text-muted)',
                  cursor: 'pointer',
                  fontWeight: user.role === r ? 600 : 400,
                  transition: 'all 0.15s ease'
                }}
              >
                {r}
              </button>
            ))}
          </div>

          {/* User Badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingLeft: '8px', borderLeft: '1px solid var(--border-color)' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#FFFFFF' }}>{user.name}</div>
              <div style={{ fontSize: '10px', color: '#818CF8', display: 'flex', alignItems: 'center', gap: '3px', justifyContent: 'flex-end' }}>
                <ShieldCheck size={10} /> {user.role}
              </div>
            </div>
            <button
              onClick={onLogout}
              title="Logout"
              style={{
                background: 'rgba(244, 63, 94, 0.1)',
                border: '1px solid rgba(244, 63, 94, 0.2)',
                color: '#F43F5E',
                width: '34px',
                height: '34px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

import React, { useState } from 'react';
import { Bot, Lock, Mail, ShieldAlert, ArrowRight } from 'lucide-react';
import { axiosInstance } from '../api/axiosInstance';
import type { User, Role } from '../types';

interface LoginPageProps {
  onLoginSuccess: (token: string, user: User) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('admin@enterprise.com');
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res: any = await axiosInstance.post('/auth/login', { email, password });
      if (res.success && res.data) {
        onLoginSuccess(res.data.token, res.data.user);
      } else {
        setError(res.message || 'Login failed');
      }
    } catch (err: any) {
      // Mock Fallback for UI responsiveness
      const mockRole: Role = email.includes('admin') ? 'Admin' : email.includes('manager') ? 'Manager' : email.includes('analyst') ? 'Analyst' : 'Executive';
      const mockUser: User = {
        id: 'usr_demo',
        email,
        name: email.split('@')[0].toUpperCase(),
        role: mockRole,
        permissions: ['view_dashboard', 'run_decision', 'approve_decision', 'manage_users', 'run_simulation'],
      };
      onLoginSuccess('demo_jwt_token_123', mockUser);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (role: Role) => {
    const roleEmailMap: Record<Role, string> = {
      Admin: 'admin@enterprise.com',
      Manager: 'manager@enterprise.com',
      Analyst: 'analyst@enterprise.com',
      Executive: 'executive@enterprise.com',
    };
    setEmail(roleEmailMap[role]);
    setPassword('password123');
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at 50% 30%, rgba(99, 102, 241, 0.15) 0%, rgba(11, 15, 23, 1) 70%)',
      padding: '24px'
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '440px',
        padding: '36px',
        display: 'flex',
        flexDirection: 'column',
        gap: '24px'
      }}>
        {/* Header */}
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: '14px',
            background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px',
            boxShadow: '0 0 24px rgba(99, 102, 241, 0.5)'
          }}>
            <Bot size={30} color="#FFFFFF" />
          </div>
          <h2 style={{ fontSize: '24px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>Enterprise Sign In</h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '6px' }}>Access your AI Multi-Agent Decision Hub</p>
        </div>

        {error && (
          <div style={{
            background: 'rgba(244, 63, 94, 0.15)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            color: '#F43F5E',
            padding: '10px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <ShieldAlert size={16} />
            <span>{error}</span>
          </div>
        )}

        {/* Credentials Form */}
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ fontSize: '12px', fontWeight: 500, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Email Address</label>
            <div style={{ position: 'relative' }}>
              <Mail size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '12px', top: '12px' }} />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '10px 12px 10px 38px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  color: '#FFFFFF',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '12px', fontWeight: 500, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '12px', top: '12px' }} />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '10px 12px 10px 38px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  color: '#FFFFFF',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              marginTop: '8px',
              padding: '12px',
              background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
              border: 'none',
              borderRadius: '8px',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '14px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 16px rgba(99, 102, 241, 0.3)',
              transition: 'all 0.2s ease'
            }}
          >
            {loading ? 'Authenticating...' : 'Sign In to Dashboard'} <ArrowRight size={16} />
          </button>
        </form>

        {/* Quick Role Fill Demo Bar */}
        <div style={{ paddingTop: '16px', borderTop: '1px solid var(--border-color)' }}>
          <p style={{ fontSize: '11px', color: 'var(--text-dim)', textAlign: 'center', marginBottom: '10px' }}>Quick Demo Auto-Fill Roles:</p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            {(['Admin', 'Manager', 'Analyst', 'Executive'] as Role[]).map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => handleQuickFill(r)}
                style={{
                  fontSize: '11px',
                  padding: '6px 10px',
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '6px',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  textAlign: 'center'
                }}
              >
                {r} Mode
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

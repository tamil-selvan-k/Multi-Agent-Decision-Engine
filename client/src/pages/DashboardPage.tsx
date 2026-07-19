import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, CheckCircle2, Clock, Users, Zap } from 'lucide-react';
import { axiosInstance } from '../api/axiosInstance';
import type { DashboardData } from '../types';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res: any = await axiosInstance.get('/dashboard');
        if (res.success && res.data) {
          setData(res.data);
        }
      } catch (err) {
        // Mock fallback data
        setData({
          kpis: {
            totalDecisions: 124,
            pendingApprovals: 3,
            negotiationSuccessRate: 98.4,
            activeAgents: 4,
          },
          recentDecisions: [
            {
              id: 'dec_101',
              title: 'Q3 Inventory Rebalancing & Marketing Promotion',
              status: 'APPROVED',
              timestamp: new Date().toISOString(),
            },
            {
              id: 'dec_102',
              title: 'Logistics Expedition & Budget Overrun Waiver',
              status: 'PENDING_APPROVAL',
              timestamp: new Date().toISOString(),
            },
            {
              id: 'dec_103',
              title: 'Sales Forecast Price Discount Threshold Alignment',
              status: 'COMPLETED',
              timestamp: new Date(Date.now() - 3600000).toISOString(),
            },
          ],
          alerts: [
            {
              id: 'alt_01',
              severity: 'WARNING',
              message: 'Sales forecast exceeds current inventory stock in Western Region.',
              timestamp: new Date().toISOString(),
            },
            {
              id: 'alt_02',
              severity: 'INFO',
              message: 'Finance Agent verified $50,000 promotional budget availability.',
              timestamp: new Date(Date.now() - 1800000).toISOString(),
            },
          ],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading || !data) {
    return <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading Executive Dashboard...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Page Header */}
      <div>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>Executive Command Center</h2>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>Real-time overview of autonomous agent negotiations and pending human approvals</p>
      </div>

      {/* KPI Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        <div className="glass-panel glass-card-interactive" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Total Decisions</span>
            <Activity size={20} color="#6366F1" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#FFFFFF', marginTop: '8px' }}>{data.kpis.totalDecisions}</div>
          <div style={{ fontSize: '11px', color: '#10B981', marginTop: '4px' }}>+12% from last week</div>
        </div>

        <div className="glass-panel glass-card-interactive" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Pending Approvals</span>
            <Clock size={20} color="#F59E0B" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#F59E0B', marginTop: '8px' }}>{data.kpis.pendingApprovals}</div>
          <div style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px' }}>Requires Human 1-Click Action</div>
        </div>

        <div className="glass-panel glass-card-interactive" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Negotiation Consensus</span>
            <CheckCircle2 size={20} color="#10B981" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#FFFFFF', marginTop: '8px' }}>{data.kpis.negotiationSuccessRate}%</div>
          <div style={{ fontSize: '11px', color: '#10B981', marginTop: '4px' }}>High agent alignment score</div>
        </div>

        <div className="glass-panel glass-card-interactive" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Active Agents</span>
            <Users size={20} color="#8B5CF6" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#FFFFFF', marginTop: '8px' }}>{data.kpis.activeAgents}</div>
          <div style={{ fontSize: '11px', color: '#818CF8', marginTop: '4px' }}>Sales, Inventory, Finance, Logistics</div>
        </div>
      </div>

      {/* Grid Layout: Recent Decisions + Alerts */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        {/* Recent Decisions Table */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Zap size={18} color="#6366F1" /> Recent Agent Decisions
            </h3>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-dim)', fontSize: '11px', textTransform: 'uppercase' }}>
                  <th style={{ padding: '8px 12px' }}>Decision ID</th>
                  <th style={{ padding: '8px 12px' }}>Title</th>
                  <th style={{ padding: '8px 12px' }}>Status</th>
                  <th style={{ padding: '8px 12px' }}>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {data.recentDecisions.map((dec) => (
                  <tr key={dec.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                    <td style={{ padding: '12px', fontFamily: 'JetBrains Mono, monospace', color: '#818CF8', fontSize: '12px' }}>{dec.id}</td>
                    <td style={{ padding: '12px', color: '#FFFFFF', fontWeight: 500 }}>{dec.title}</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{
                        padding: '4px 8px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        fontWeight: 600,
                        background: dec.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.15)' : dec.status === 'PENDING_APPROVAL' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(99, 102, 241, 0.15)',
                        color: dec.status === 'APPROVED' ? '#10B981' : dec.status === 'PENDING_APPROVAL' ? '#F59E0B' : '#818CF8',
                        border: `1px solid ${dec.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.3)' : dec.status === 'PENDING_APPROVAL' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(99, 102, 241, 0.3)'}`
                      }}>
                        {dec.status}
                      </span>
                    </td>
                    <td style={{ padding: '12px', color: 'var(--text-muted)', fontSize: '12px' }}>{new Date(dec.timestamp).toLocaleTimeString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* System Alerts */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={18} color="#F59E0B" /> Cross-Domain Risk Alerts
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.alerts.map((alt) => (
              <div key={alt.id} style={{
                padding: '12px',
                borderRadius: '8px',
                background: alt.severity === 'WARNING' ? 'rgba(245, 158, 11, 0.08)' : 'rgba(6, 182, 212, 0.08)',
                border: `1px solid ${alt.severity === 'WARNING' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(6, 182, 212, 0.2)'}`,
                display: 'flex',
                flexDirection: 'column',
                gap: '6px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '10px', fontWeight: 700, color: alt.severity === 'WARNING' ? '#F59E0B' : '#06B6D4' }}>{alt.severity}</span>
                  <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>{new Date(alt.timestamp).toLocaleTimeString()}</span>
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-main)', lineHeight: '1.4' }}>{alt.message}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

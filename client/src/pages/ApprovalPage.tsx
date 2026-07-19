import React, { useState } from 'react';
import { CheckCircle2, XCircle, ShieldCheck } from 'lucide-react';
import { axiosInstance } from '../api/axiosInstance';

export const ApprovalPage: React.FC = () => {
  const [approvals, setApprovals] = useState([
    {
      id: 'dec_102',
      title: 'Logistics Expedition & Budget Overrun Waiver',
      summary: 'Authorize $5,000 budget shift from Marketing to Logistics for 3-day expedited freight delivery.',
      agents: ['LogisticsAgent (Req)', 'FinanceAgent (Appr)', 'SalesAgent (Impacted)'],
      risk: 'LOW',
      status: 'PENDING_APPROVAL',
      amount: '$5,000 USD',
    },
    {
      id: 'dec_104',
      title: 'Emergency Inventory Buffer Expansion',
      summary: 'Reorder 1,000 additional units from primary supplier due to high demand forecast in Southern Region.',
      agents: ['SalesAgent', 'InventoryAgent'],
      risk: 'MEDIUM',
      status: 'PENDING_APPROVAL',
      amount: '$18,500 USD',
    },
  ]);

  const handleAction = async (id: string, action: 'approve' | 'reject') => {
    try {
      await axiosInstance.post(`/approval/${id}`, { action });
    } catch (err) {
      // Ignore network errors in demo mode
    }

    setApprovals((prev) =>
      prev.map((item) =>
        item.id === id
          ? { ...item, status: action === 'approve' ? 'APPROVED' : 'REJECTED' }
          : item
      )
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>Human-on-the-Loop Approvals</h2>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>Review and sign-off on autonomous multi-agent operational decisions</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {approvals.map((item) => (
          <div key={item.id} className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '12px', fontFamily: 'JetBrains Mono, monospace', color: '#818CF8', fontWeight: 600 }}>{item.id}</span>
                <h3 style={{ fontSize: '16px', fontWeight: 600, color: '#FFFFFF', margin: 0 }}>{item.title}</h3>
              </div>

              <span style={{
                fontSize: '11px',
                fontWeight: 700,
                padding: '4px 10px',
                borderRadius: '6px',
                background: item.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.15)' : item.status === 'REJECTED' ? 'rgba(244, 63, 94, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                color: item.status === 'APPROVED' ? '#10B981' : item.status === 'REJECTED' ? '#F43F5E' : '#F59E0B',
                border: `1px solid ${item.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.3)' : item.status === 'REJECTED' ? 'rgba(244, 63, 94, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`
              }}>
                {item.status}
              </span>
            </div>

            <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: '1.5' }}>{item.summary}</p>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.05)', fontSize: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <span style={{ color: 'var(--text-dim)' }}>Value Impact: <strong style={{ color: '#FFFFFF' }}>{item.amount}</strong></span>
                <span style={{ color: 'var(--text-dim)' }}>Risk Level: <strong style={{ color: item.risk === 'LOW' ? '#10B981' : '#F59E0B' }}>{item.risk}</strong></span>
              </div>

              {item.status === 'PENDING_APPROVAL' ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <button
                    onClick={() => handleAction(item.id, 'reject')}
                    style={{
                      padding: '8px 16px',
                      borderRadius: '8px',
                      background: 'rgba(244, 63, 94, 0.1)',
                      border: '1px solid rgba(244, 63, 94, 0.3)',
                      color: '#F43F5E',
                      fontSize: '12px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px'
                    }}
                  >
                    <XCircle size={16} /> Reject Decision
                  </button>
                  <button
                    onClick={() => handleAction(item.id, 'approve')}
                    style={{
                      padding: '8px 18px',
                      borderRadius: '8px',
                      background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
                      border: 'none',
                      color: '#FFFFFF',
                      fontSize: '12px',
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      boxShadow: '0 4px 14px rgba(16, 185, 129, 0.3)'
                    }}
                  >
                    <CheckCircle2 size={16} /> Approve Plan
                  </button>
                </div>
              ) : (
                <span style={{ fontSize: '12px', color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <ShieldCheck size={14} color="#10B981" /> Action Logged Permanently
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

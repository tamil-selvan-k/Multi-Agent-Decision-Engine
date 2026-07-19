import React, { useState } from 'react';
import { SlidersHorizontal, Play, BarChart3, AlertTriangle, ArrowUpRight, DollarSign } from 'lucide-react';
import { axiosInstance } from '../api/axiosInstance';
import type { SimulationResult } from '../types';

export const SimulationPage: React.FC = () => {
  const [demandIncrease, setDemandIncrease] = useState(20);
  const [budgetReduction, setBudgetReduction] = useState(10);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);

  const handleRunSimulation = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res: any = await axiosInstance.post('/simulation', {
        demandIncrease,
        budgetReduction,
      });
      if (res.success && res.data) {
        setResult(res.data);
      }
    } catch (err) {
      // Mock Fallback
      setResult({
        scenarioInput: {
          demandIncreasePercent: demandIncrease,
          budgetReductionPercent: budgetReduction,
        },
        simulationResults: {
          projectedRevenueImpactPercent: Number(((demandIncrease * 1.5) - (budgetReduction * 0.8)).toFixed(2)),
          projectedInventoryStockoutRisk: demandIncrease > 30 ? 'HIGH' : budgetReduction > 15 ? 'MEDIUM' : 'LOW',
          recommendedReallocation: {
            expeditedFreightBudget: `$${(budgetReduction * 500).toLocaleString()}`,
            bufferStockUnits: demandIncrease * 50,
          },
          agentsConsensus: 'MODERATE_CONFIDENCE',
        },
        timestamp: new Date().toISOString(),
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>What-If Market Simulator</h2>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>Test operational scenarios and preview multi-agent consensus recommendations</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Sliders Configuration Panel */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <SlidersHorizontal size={18} color="#6366F1" /> Scenario Parameters
          </h3>

          {/* Slider 1: Demand Increase */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Demand Increase (%)</span>
              <span style={{ color: '#818CF8', fontWeight: 700 }}>+{demandIncrease}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="50"
              value={demandIncrease}
              onChange={(e) => setDemandIncrease(Number(e.target.value))}
              style={{ accentColor: '#6366F1', cursor: 'pointer' }}
            />
          </div>

          {/* Slider 2: Budget Reduction */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Budget Reduction (%)</span>
              <span style={{ color: '#F43F5E', fontWeight: 700 }}>-{budgetReduction}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="50"
              value={budgetReduction}
              onChange={(e) => setBudgetReduction(Number(e.target.value))}
              style={{ accentColor: '#F43F5E', cursor: 'pointer' }}
            />
          </div>

          <button
            onClick={handleRunSimulation}
            disabled={loading}
            style={{
              marginTop: '12px',
              padding: '12px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
              border: 'none',
              color: '#FFFFFF',
              fontWeight: 700,
              fontSize: '13px',
              cursor: loading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 16px rgba(99, 102, 241, 0.3)'
            }}
          >
            <Play size={16} fill="#FFFFFF" /> {loading ? 'Simulating Scenario...' : 'Execute Simulation Run'}
          </button>
        </div>

        {/* Output Projection Results */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <BarChart3 size={18} color="#10B981" /> Simulation Output Projection
          </h3>

          {result ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ padding: '16px', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Projected Revenue Impact</div>
                <div style={{ fontSize: '24px', fontWeight: 800, color: '#10B981', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  +{result.simulationResults.projectedRevenueImpactPercent}% <ArrowUpRight size={22} />
                </div>
              </div>

              <div style={{ padding: '16px', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Inventory Stockout Risk</div>
                <div style={{ fontSize: '20px', fontWeight: 700, color: '#F59E0B', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <AlertTriangle size={20} /> {result.simulationResults.projectedInventoryStockoutRisk} RISK
                </div>
              </div>

              <div style={{ padding: '14px', borderRadius: '8px', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', fontSize: '12px' }}>
                <div style={{ fontWeight: 600, color: '#FFFFFF', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <DollarSign size={14} color="#818CF8" /> Agent Recommended Reallocation
                </div>
                <div style={{ color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  • Expedited Freight Budget: <strong style={{ color: '#FFFFFF' }}>{result.simulationResults.recommendedReallocation.expeditedFreightBudget}</strong><br />
                  • Buffer Stock Reserve: <strong style={{ color: '#FFFFFF' }}>{result.simulationResults.recommendedReallocation.bufferStockUnits} units</strong>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-dim)', fontSize: '13px' }}>
              Adjust parameters and click "Execute Simulation Run" to preview multi-agent recommendations.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

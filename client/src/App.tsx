import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, type TabType } from './components/Sidebar';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { DepartmentsPage } from './pages/DepartmentsPage';
import { DecisionPage } from './pages/DecisionPage';
import { ApprovalPage } from './pages/ApprovalPage';
import { SimulationPage } from './pages/SimulationPage';
import type { User, Role } from './types';

export function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token') || 'demo_token');
  const [user, setUser] = useState<User | null>({
    id: 'usr_admin',
    email: 'admin@enterprise.com',
    name: 'Sarah Connor (Executive)',
    role: 'Admin',
    permissions: ['view_dashboard', 'run_decision', 'approve_decision', 'manage_users', 'run_simulation'],
  });

  const [activeTab, setActiveTab] = useState<TabType>('dashboard');

  const handleLoginSuccess = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const handleSwitchRole = (newRole: Role) => {
    if (!user) return;
    setUser({
      ...user,
      role: newRole,
      name: `${user.name.split(' (')[0]} (${newRole})`,
    });
  };

  if (!token || !user) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', background: 'var(--bg-dark)' }}>
      {/* Top Navbar */}
      <Navbar user={user} onLogout={handleLogout} onSwitchRole={handleSwitchRole} />

      {/* Main Layout Container */}
      <div style={{ display: 'flex', flex: 1 }}>
        {/* Navigation Sidebar */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} pendingApprovalsCount={2} />

        {/* Dynamic View Content */}
        <main style={{ flex: 1, padding: '28px', maxWidth: '1280px', margin: '0 auto', width: '100%' }}>
          {activeTab === 'dashboard' && <DashboardPage />}
          {activeTab === 'departments' && <DepartmentsPage />}
          {activeTab === 'decision' && <DecisionPage />}
          {activeTab === 'approval' && <ApprovalPage />}
          {activeTab === 'simulation' && <SimulationPage />}
        </main>
      </div>
    </div>
  );
}

export default App;

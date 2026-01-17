import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import { useAppStore } from '../store';
import api from '../api';

const Dashboard: React.FC = () => {
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions } = useAppStore();
  const [healthStatus, setHealthStatus] = useState<string>('Checking...');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        await Promise.all([
          fetchProductions(),
          fetchJurisdictions(),
        ]);
        
        // Check health
        try {
          const health = await api.health();
          setHealthStatus(health.status);
        } catch {
          setHealthStatus('Offline');
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [fetchProductions, fetchJurisdictions]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Overview of your tax incentive platform</p>
        </div>
        <div className="text-sm">
          <span className="text-gray-600">API Status: </span>
          <span className={`font-semibold ${healthStatus === 'healthy' ? 'text-green-600' : 'text-red-600'}`}>
            {healthStatus}
          </span>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="text-center">
            <p className="text-gray-500 text-sm uppercase font-semibold">Active Productions</p>
            <p className="text-4xl font-bold text-pilotforge-blue mt-2">{productions.length}</p>
          </div>
        </Card>

        <Card>
          <div className="text-center">
            <p className="text-gray-500 text-sm uppercase font-semibold">Jurisdictions</p>
            <p className="text-4xl font-bold text-pilotforge-blue mt-2">{jurisdictions.length}</p>
          </div>
        </Card>

        <Card>
          <div className="text-center">
            <p className="text-gray-500 text-sm uppercase font-semibold">Tax Programs</p>
            <p className="text-4xl font-bold text-pilotforge-blue mt-2">33+</p>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card title="Quick Actions">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Button 
            variant="primary" 
            onClick={() => window.location.href = '/productions'}
            className="w-full"
          >
            Create New Production
          </Button>
          <Button 
            variant="secondary" 
            onClick={() => window.location.href = '/calculator'}
            className="w-full"
          >
            Calculate Incentives
          </Button>
        </div>
      </Card>

      {/* Recent Productions */}
      <Card title="Recent Productions" subtitle={`${productions.length} total production${productions.length !== 1 ? 's' : ''}`}>
        {productions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No productions yet. Create your first production to get started.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {productions.slice(0, 5).map((production) => (
              <div key={production.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900">{production.title}</p>
                  <p className="text-sm text-gray-600">
                    Budget: ${production.budget.toLocaleString()}
                  </p>
                </div>
                <Button size="sm" variant="secondary">
                  View Details
                </Button>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Jurisdiction Coverage */}
      <Card title="Jurisdiction Coverage" subtitle="Global tax incentive programs">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {jurisdictions.slice(0, 8).map((jurisdiction) => (
            <div key={jurisdiction.id} className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="font-semibold text-gray-900">{jurisdiction.code}</p>
              <p className="text-xs text-gray-600 mt-1">{jurisdiction.name}</p>
            </div>
          ))}
          {jurisdictions.length > 8 && (
            <div className="text-center p-3 bg-pilotforge-blue text-white rounded-lg flex items-center justify-center">
              <p className="font-semibold">+{jurisdictions.length - 8} more</p>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;

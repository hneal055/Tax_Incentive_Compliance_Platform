import React, { useEffect, useState } from 'react';
import { Film, Plus, DollarSign, Calendar, Building2, MapPin } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import CreateProductionModal from '../components/CreateProductionModal';
import { useAppStore } from '../store';

const Productions: React.FC = () => {
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions, isLoading } = useAppStore();
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  const handleProductionCreated = () => {
    fetchProductions();
  };

  if (isLoading && productions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Create Production Modal */}
      <CreateProductionModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        jurisdictions={jurisdictions}
        onSuccess={handleProductionCreated}
      />

      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
            Productions
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your film and TV productions</p>
        </div>
        <Button 
          onClick={() => setShowCreateModal(true)}
          icon={Plus}
        >
          New Production
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {productions.length === 0 ? (
          <div className="col-span-full">
            <Card>
              <EmptyState
                icon={Film}
                title="No productions yet"
                description="Create your first production to start tracking tax incentives, managing budgets, and ensuring compliance."
                actionLabel="Create your first production"
                onAction={() => setShowCreateModal(true)}
              />
            </Card>
          </div>
        ) : (
          productions.map((production, index) => (
            <div
              key={production.id}
              className="animate-fade-in"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <Card 
                title={production.title}
                hoverable
                className="h-full"
              >
                <div className="space-y-3">
                  {production.productionType && (
                    <div className="flex items-center gap-2 text-sm">
                      <span className="px-2 py-1 rounded-full bg-accent-blue/10 text-accent-blue dark:bg-accent-teal/10 dark:text-accent-teal font-medium text-xs uppercase">
                        {production.productionType.replace('_', ' ')}
                      </span>
                      {production.status && (
                        <span className="px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 font-medium text-xs">
                          {production.status.replace('_', ' ')}
                        </span>
                      )}
                    </div>
                  )}
                  <div className="flex items-center justify-between p-3 bg-gradient-to-br from-accent-blue/5 to-accent-teal/5 dark:from-accent-blue/10 dark:to-accent-teal/10 rounded-lg">
                    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                      <DollarSign className="h-4 w-4" />
                      <span>Budget</span>
                    </div>
                    <span className="font-bold text-lg text-gray-900 dark:text-gray-100">
                      ${(production.budgetTotal || production.budget).toLocaleString()}
                    </span>
                  </div>
                  {production.productionCompany && (
                    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                      <Building2 className="h-4 w-4" />
                      <span>{production.productionCompany}</span>
                    </div>
                  )}
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                      <Calendar className="h-4 w-4" />
                      <span>Created</span>
                    </div>
                    <span className="text-gray-900 dark:text-gray-100 font-medium">
                      {new Date(production.created_at || production.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <Button size="sm" variant="outline" className="w-full">
                    View Details →
                  </Button>
                </div>
              </Card>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Productions;

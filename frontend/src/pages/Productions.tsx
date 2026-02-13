import React, { useEffect, useState, useMemo } from 'react';
import { 
  Film, Plus, DollarSign, Calendar, Building2, Search, Filter, X, 
  TrendingUp
} from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import CreateProductionModal from '../components/CreateProductionModal';
import { useAppStore } from '../store';
import type { Production } from '../types';

const Productions: React.FC = () => {
  const { 
    productions, jurisdictions, fetchProductions, fetchJurisdictions, 
    isLoading, selectedProduction, selectProduction 
  } = useAppStore();

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isDetailOpen, setIsDetailOpen] = useState(!!selectedProduction);

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  const filteredProductions = useMemo(() => {
    return productions.filter(p => {
      const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                           (p.productionCompany?.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesStatus = statusFilter === 'all' || p.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  }, [productions, searchQuery, statusFilter]);

  const handleViewDetails = (production: Production) => {
    selectProduction(production);
    setIsDetailOpen(true);
  };

  const closeDetails = () => {
    setIsDetailOpen(false);
    selectProduction(null);
  };

  const getPerformanceData = (production: Production) => {
    const budget = production.budgetTotal || production.budget || 1000000;
    const estIncentive = budget * 0.25;
    const actualIncentive = budget * 0.245;
    const variance = ((actualIncentive - estIncentive) / estIncentive) * 100;
    return {
      estimated: estIncentive,
      actual: actualIncentive,
      variance: variance.toFixed(1),
      isPositive: variance >= 0,
      progress: '98%'
    };
  };

  if (isLoading && productions.length === 0) {
    return <div className="flex justify-center items-center h-64"><Spinner size="lg" /></div>;
  }

  return (
    <>
      {/* Modal rendered outside page layout — uses portal internally */}
      <CreateProductionModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        jurisdictions={jurisdictions}
        onSuccess={fetchProductions}
      />

      <div className="space-y-6 py-6 px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">Productions</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Manage film and TV productions and track compliance.</p>
          </div>
          <Button onClick={() => setShowCreateModal(true)} icon={Plus}>New Production</Button>
        </div>

        <div className="flex flex-col md:flex-row gap-4 bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search productions..."
              title="Search productions"
              className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
              <select
                title="Filter by Status"
                className="pl-10 pr-8 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-accent-blue outline-none appearance-none text-sm font-bold"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="all">All Statuses</option>
                <option value="PRE_PRODUCTION">Pre-Production</option>
                <option value="PRODUCTION">In Production</option>
                <option value="POST_PRODUCTION">Post-Production</option>
                <option value="COMPLETED">Completed</option>
              </select>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProductions.length === 0 ? (
            <div className="col-span-full">
              <Card>
                <EmptyState
                  icon={Film}
                  title="No productions found"
                  description="Try adjusting your search or create a new production."
                  actionLabel="Create Production"
                  onAction={() => setShowCreateModal(true)}
                />
              </Card>
            </div>
          ) : (
            filteredProductions.map((production) => (
              <Card key={production.id} title={production.title} hoverable>
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {production.productionType && (
                      <span className="px-2 py-0.5 rounded bg-accent-blue/10 text-accent-blue text-[10px] font-bold uppercase tracking-wider">
                        {production.productionType.replace('_', ' ')}
                      </span>
                    )}
                    {production.status && (
                      <span className="px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-[10px] font-bold uppercase tracking-wider">
                        {production.status.replace('_', ' ')}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
                    <div className="flex items-center gap-2 text-sm text-gray-500"><DollarSign className="h-4 w-4" /><span>Budget</span></div>
                    <span className="font-bold text-gray-900 dark:text-gray-100">${(production.budgetTotal || production.budget || 0).toLocaleString()}</span>
                  </div>
                  <div className="space-y-1">
                    {production.productionCompany && (
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400"><Building2 className="h-4 w-4" /><span className="truncate">{production.productionCompany}</span></div>
                    )}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center gap-2"><Calendar className="h-4 w-4" /><span>Created</span></div>
                      <span>{new Date(production.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
                    <Button size="sm" variant="outline" className="w-full" onClick={() => handleViewDetails(production)}>View Details</Button>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>

        {/* Production detail slide-over panel */}
        {isDetailOpen && selectedProduction && (
          <div className="fixed inset-0 flex justify-end" style={{ zIndex: 9998 }}>
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={closeDetails} />
            <div className="relative w-full max-w-xl bg-white dark:bg-gray-900 h-full shadow-2xl flex flex-col p-6 animate-fade-in overflow-hidden">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{selectedProduction.title}</h2>
                  <p className="text-gray-500">{selectedProduction.productionCompany || 'Project'}</p>
                </div>
                <button 
                  onClick={closeDetails} 
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
                  aria-label="Close details"
                >
                  <X className="h-5 w-5 text-gray-500" />
                </button>
              </div>
              
              <div className="space-y-8 flex-1 overflow-y-auto">
                <section>
                  <div className="flex items-center gap-2 mb-4"><TrendingUp className="h-5 w-5 text-accent-blue" /><h3 className="font-bold dark:text-white">Incentive Performance</h3></div>
                  {(() => {
                    const perf = getPerformanceData(selectedProduction);
                    return (
                      <div className="p-4 bg-accent-blue/5 dark:bg-accent-teal/5 border border-accent-blue/10 rounded-xl">
                        <div className="flex justify-between items-end mb-4">
                          <div><p className="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Estimated Incentives</p><p className="text-3xl font-black dark:text-white">${perf.actual.toLocaleString(undefined, { maximumFractionDigits: 0 })}</p></div>
                          <div className={`text-sm font-bold ${perf.isPositive ? 'text-status-active' : 'text-status-error'}`}>{perf.variance}%</div>
                        </div>
                        <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div className="h-full bg-accent-blue w-[98%]" />
                        </div>
                      </div>
                    );
                  })()}
                </section>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"><p className="text-[10px] uppercase font-bold text-gray-400 mb-1">Status</p><p className="font-semibold dark:text-white">{selectedProduction.status?.replace('_', ' ')}</p></div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"><p className="text-[10px] uppercase font-bold text-gray-400 mb-1">Type</p><p className="font-semibold dark:text-white">{selectedProduction.productionType?.replace('_', ' ')}</p></div>
                </div>
              </div>
              <div className="mt-auto pt-6 border-t border-gray-200 dark:border-gray-800"><Button variant="primary" className="w-full" onClick={closeDetails}>Close Details</Button></div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Productions;

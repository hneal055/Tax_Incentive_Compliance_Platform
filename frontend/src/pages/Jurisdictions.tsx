import { Globe, Building2, MapPin } from 'lucide-react';
import Card from '../components/Card';
import EmptyState from '../components/EmptyState';
import { motion } from 'framer-motion';
import type { Production } from '../types';

interface JurisdictionsProps {
  productions: Production[];
  onAddProduction?: (production: Production) => void;
  onUpdateProduction?: (production: Production) => void;
  onDeleteProduction?: (id: string) => void;
}

function Jurisdictions({}: JurisdictionsProps) {
  // Mock jurisdictions data
  const jurisdictions = [
    { id: '1', code: 'CA', name: 'California', country: 'United States', type: 'State' },
    { id: '2', code: 'GA', name: 'Georgia', country: 'United States', type: 'State' },
    { id: '3', code: 'LA', name: 'Louisiana', country: 'United States', type: 'State' },
    { id: '4', code: 'NY', name: 'New York', country: 'United States', type: 'State' },
    { id: '5', code: 'BC', name: 'British Columbia', country: 'Canada', type: 'Province' },
    { id: '6', code: 'ON', name: 'Ontario', country: 'Canada', type: 'Province' },
    { id: '7', code: 'GB', name: 'United Kingdom', country: 'United Kingdom', type: 'Country' },
    { id: '8', code: 'AU', name: 'Australia', country: 'Australia', type: 'Country' },
  ];

  const getTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'state':
      case 'province':
        return Building2;
      case 'country':
        return Globe;
      default:
        return MapPin;
    }
  };

  const getTypeBadgeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'state':
      case 'province':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
      case 'country':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400';
      default:
        return 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-[28px] font-bold text-slate-900 tracking-tight">
          Jurisdictions
        </h1>
        <p className="text-slate-500 mt-1.5 text-[15px]">
          {jurisdictions.length} global jurisdictions with tax incentive programs
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jurisdictions.length === 0 ? (
          <div className="col-span-full">
            <Card>
              <EmptyState
                icon={MapPin}
                title="No jurisdictions available"
                description="Jurisdiction data will be loaded from the API. Please check your connection and ensure the backend is running."
                actionLabel="Retry loading"
                onAction={() => {}}
              />
            </Card>
          </div>
        ) : (
          jurisdictions.map((jurisdiction, index) => {
            const TypeIcon = getTypeIcon(jurisdiction.type);
            return (
              <motion.div
                key={jurisdiction.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.03 }}
              >
                <Card hoverable className="h-full">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-gradient-to-br from-blue-100/50 to-cyan-100/50 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-lg">
                          <TypeIcon className="h-5 w-5 text-blue-600 dark:text-cyan-400" />
                        </div>
                        <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-400 bg-clip-text text-transparent">
                          {jurisdiction.code}
                        </span>
                      </div>
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getTypeBadgeColor(jurisdiction.type)}`}>
                        {jurisdiction.type}
                      </span>
                    </div>
                    <div className="space-y-2">
                      <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
                        {jurisdiction.name}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <Globe className="h-4 w-4" />
                        <span>{jurisdiction.country}</span>
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default Jurisdictions;

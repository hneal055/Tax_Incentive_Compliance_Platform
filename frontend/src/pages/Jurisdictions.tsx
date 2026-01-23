import React, { useEffect } from 'react';
import { MapPin, Globe, Building2 } from 'lucide-react';
import Card from '../components/Card';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import { useAppStore } from '../store';
import { motion } from 'framer-motion';

const Jurisdictions: React.FC = () => {
  const { jurisdictions, fetchJurisdictions, isLoading } = useAppStore();

  useEffect(() => {
    fetchJurisdictions();
  }, [fetchJurisdictions]);

  if (isLoading && jurisdictions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

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
        return 'bg-accent-blue/20 text-accent-blue dark:bg-accent-blue/30 dark:text-accent-blue';
      case 'country':
        return 'bg-accent-emerald/20 text-accent-emerald dark:bg-accent-emerald/30 dark:text-accent-emerald';
      default:
        return 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Jurisdictions
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
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
                onAction={fetchJurisdictions}
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
                        <div className="p-2 bg-gradient-to-br from-accent-blue/20 to-accent-teal/20 dark:from-accent-blue/30 dark:to-accent-teal/30 rounded-lg">
                          <TypeIcon className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
                        </div>
                        <span className="text-3xl font-bold bg-gradient-to-r from-accent-blue to-accent-teal bg-clip-text text-transparent">
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
};

export default Jurisdictions;

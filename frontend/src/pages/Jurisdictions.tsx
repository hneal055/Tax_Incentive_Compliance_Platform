import React, { useEffect } from 'react';
import Card from '../components/Card';
import Spinner from '../components/Spinner';
import { useAppStore } from '../store';

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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Jurisdictions</h1>
        <p className="text-gray-600 mt-1">
          {jurisdictions.length} global jurisdictions with tax incentive programs
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jurisdictions.length === 0 ? (
          <Card className="col-span-full">
            <div className="text-center py-12 text-gray-500">
              <p>No jurisdictions available</p>
            </div>
          </Card>
        ) : (
          jurisdictions.map((jurisdiction) => (
            <Card key={jurisdiction.id}>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-pilotforge-blue">
                    {jurisdiction.code}
                  </span>
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                    {jurisdiction.type}
                  </span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{jurisdiction.name}</h3>
                  <p className="text-sm text-gray-600">{jurisdiction.country}</p>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default Jurisdictions;

import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';
import Spinner from '../components/Spinner';
import { useAppStore } from '../store';

const Productions: React.FC = () => {
  const { productions, fetchProductions, createProduction, isLoading } = useAppStore();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    budget: '',
  });

  useEffect(() => {
    fetchProductions();
  }, [fetchProductions]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createProduction({
      title: formData.title,
      budget: parseFloat(formData.budget),
    });
    setFormData({ title: '', budget: '' });
    setShowForm(false);
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Productions</h1>
          <p className="text-gray-600 mt-1">Manage your film and TV productions</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'New Production'}
        </Button>
      </div>

      {showForm && (
        <Card title="Create New Production">
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Production Title"
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Enter production title"
              required
            />
            <Input
              label="Budget ($)"
              type="number"
              value={formData.budget}
              onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
              placeholder="Enter budget amount"
              required
              min="0"
              step="0.01"
            />
            <div className="flex space-x-2">
              <Button type="submit" className="flex-1">Create Production</Button>
              <Button type="button" variant="secondary" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {productions.length === 0 ? (
          <Card className="col-span-full">
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg mb-4">No productions yet</p>
              <Button onClick={() => setShowForm(true)}>Create Your First Production</Button>
            </div>
          </Card>
        ) : (
          productions.map((production) => (
            <Card key={production.id} title={production.title}>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Budget:</span>
                  <span className="font-semibold">${production.budget.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Created:</span>
                  <span className="text-gray-900">
                    {new Date(production.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-200">
                <Button size="sm" className="w-full">View Details</Button>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default Productions;

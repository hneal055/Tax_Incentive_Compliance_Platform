import React, { useEffect, useState } from 'react';
import { Film, Plus, DollarSign, Calendar } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
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
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
            Productions
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your film and TV productions</p>
        </div>
        <Button 
          onClick={() => setShowForm(!showForm)}
          icon={showForm ? undefined : Plus}
          variant={showForm ? 'secondary' : 'primary'}
        >
          {showForm ? 'Cancel' : 'New Production'}
        </Button>
      </div>

      {showForm && (
        <div className="animate-fade-in">
          <Card title="Create New Production" subtitle="Enter production details to start tracking incentives">
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
                <Button type="submit" className="flex-1" icon={Plus}>
                  Create Production
                </Button>
                <Button type="button" variant="secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {productions.length === 0 ? (
          <div className="col-span-full">
            <Card>
              <EmptyState
                icon={Film}
                title="No productions yet"
                description="Create your first production to start tracking tax incentives, managing budgets, and ensuring compliance."
                actionLabel="Create your first production"
                onAction={() => setShowForm(true)}
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
                  <div className="flex items-center justify-between p-3 bg-gradient-to-br from-accent-blue/5 to-accent-teal/5 dark:from-accent-blue/10 dark:to-accent-teal/10 rounded-lg">
                    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                      <DollarSign className="h-4 w-4" />
                      <span>Budget</span>
                    </div>
                    <span className="font-bold text-lg text-gray-900 dark:text-gray-100">
                      ${production.budget.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                      <Calendar className="h-4 w-4" />
                      <span>Created</span>
                    </div>
                    <span className="text-gray-900 dark:text-gray-100 font-medium">
                      {new Date(production.created_at).toLocaleDateString()}
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

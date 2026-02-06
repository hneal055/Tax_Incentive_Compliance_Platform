import React, { useState, memo } from 'react';
import { Film, DollarSign, Building2, MapPin, CheckCircle } from 'lucide-react';
import Modal from './Modal';
import Button from './Button';
import Input from './Input';
import { useAppStore } from '../store';
import type { Jurisdiction } from '../types';

interface CreateProductionModalProps {
  isOpen: boolean;
  onClose: () => void;
  jurisdictions: Jurisdiction[];
  onSuccess?: () => void;
}

const PRODUCTION_TYPES = [
  { value: 'feature', label: 'Feature Film' },
  { value: 'tv_series', label: 'TV Series' },
  { value: 'commercial', label: 'Commercial' },
  { value: 'documentary', label: 'Documentary' },
];

const CreateProductionModal: React.FC<CreateProductionModalProps> = memo(({
  isOpen,
  onClose,
  jurisdictions,
  onSuccess,
}) => {
  const { createProduction } = useAppStore();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    budget: '',
    productionType: 'feature',
    jurisdictionId: '',
    productionCompany: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      await createProduction({
        title: formData.title,
        budget: parseFloat(formData.budget),
        productionType: formData.productionType,
        jurisdictionId: formData.jurisdictionId || undefined,
        productionCompany: formData.productionCompany || undefined,
      });
      
      setSuccess(true);
      setTimeout(() => {
        setFormData({ title: '', budget: '', productionType: 'feature', jurisdictionId: '', productionCompany: '' });
        setSuccess(false);
        onSuccess?.();
        onClose();
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create production');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setFormData({ title: '', budget: '', productionType: 'feature', jurisdictionId: '', productionCompany: '' });
      setError(null);
      setSuccess(false);
      onClose();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Create New Production" size="lg">
      {success ? (
        <div className="flex flex-col items-center justify-center py-8 gap-4 animate-fade-in">
          <div className="p-4 bg-status-active/20 rounded-full">
            <CheckCircle className="h-12 w-12 text-status-active" />
          </div>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">Production Created!</p>
          <p className="text-sm text-gray-600 dark:text-gray-400">Refreshing data...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="p-3 bg-status-error/10 border border-status-error/30 rounded-lg text-sm text-status-error">
              {error}
            </div>
          )}

          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <Film className="h-4 w-4" />
              Production Title
            </label>
            <Input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Enter production title"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <DollarSign className="h-4 w-4" />
                Budget ($)
              </label>
              <Input
                type="number"
                value={formData.budget}
                onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
                placeholder="1,000,000"
                required
                min="0"
                step="1000"
              />
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Film className="h-4 w-4" />
                Production Type
              </label>
              <select
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                value={formData.productionType}
                onChange={(e) => setFormData({ ...formData, productionType: e.target.value })}
                title="Select production type"
              >
                {PRODUCTION_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <MapPin className="h-4 w-4" />
                Jurisdiction (Optional)
              </label>
              <select
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                value={formData.jurisdictionId}
                onChange={(e) => setFormData({ ...formData, jurisdictionId: e.target.value })}
                title="Select jurisdiction"
              >
                <option value="">Auto-select first available</option>
                {jurisdictions.map((jur) => (
                  <option key={jur.id} value={jur.id}>{jur.code} - {jur.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Building2 className="h-4 w-4" />
                Production Company (Optional)
              </label>
              <Input
                type="text"
                value={formData.productionCompany}
                onChange={(e) => setFormData({ ...formData, productionCompany: e.target.value })}
                placeholder="Company name"
              />
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button 
              type="button" 
              variant="secondary" 
              onClick={handleClose}
              disabled={isSubmitting}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              loading={isSubmitting}
              disabled={!formData.title || !formData.budget}
              className="flex-1"
            >
              Create Production
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
});

CreateProductionModal.displayName = 'CreateProductionModal';

export default CreateProductionModal;

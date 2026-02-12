import { useState } from 'react';
import { AlertCircle, Copy, Check, Key } from 'lucide-react';
import Button from './Button';
import Input from './Input';
import Modal from './Modal';
import type { ApiKeyCreated } from '../types';

interface CreateApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (data: { name: string; permissions: string[]; expiresAt?: string }) => Promise<ApiKeyCreated>;
}

export default function CreateApiKeyModal({ isOpen, onClose, onCreate }: CreateApiKeyModalProps) {
  const [name, setName] = useState('');
  const [permissions, setPermissions] = useState<string[]>(['read', 'write']);
  const [expiresAt, setExpiresAt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [createdKey, setCreatedKey] = useState<ApiKeyCreated | null>(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data: { name: string; permissions: string[]; expiresAt?: string } = {
        name,
        permissions,
      };
      if (expiresAt) {
        data.expiresAt = new Date(expiresAt).toISOString();
      }
      const newKey = await onCreate(data);
      setCreatedKey(newKey);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to create API key');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (createdKey?.plaintext_key) {
      await navigator.clipboard.writeText(createdKey.plaintext_key);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    setName('');
    setPermissions(['read', 'write']);
    setExpiresAt('');
    setError('');
    setCreatedKey(null);
    setCopied(false);
    onClose();
  };

  const handlePermissionToggle = (permission: string) => {
    if (permissions.includes(permission)) {
      setPermissions(permissions.filter(p => p !== permission));
    } else {
      setPermissions([...permissions, permission]);
    }
  };

  if (!isOpen) return null;

  // Show key display after creation
  if (createdKey) {
    return (
      <Modal isOpen={isOpen} onClose={handleClose} title="API Key Created">
        <div className="space-y-4">
          <div className="rounded-lg bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 p-4">
            <div className="flex gap-2">
              <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-yellow-900 dark:text-yellow-100">
                  Save your API key now!
                </h4>
                <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                  This is the only time you'll be able to see the full key. Store it securely.
                </p>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              API Key
            </label>
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Key className="h-4 w-4 text-gray-400" />
                </div>
                <input
                  type="text"
                  value={createdKey.plaintext_key}
                  readOnly
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono text-sm"
                />
              </div>
              <Button
                onClick={handleCopy}
                variant="outline"
                icon={copied ? Check : Copy}
                size="md"
              >
                {copied ? 'Copied' : 'Copy'}
              </Button>
            </div>
          </div>

          <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Name:</span>
              <span className="font-medium text-gray-900 dark:text-gray-100">{createdKey.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Permissions:</span>
              <span className="font-medium text-gray-900 dark:text-gray-100">
                {createdKey.permissions.join(', ')}
              </span>
            </div>
            {createdKey.expiresAt && (
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Expires:</span>
                <span className="font-medium text-gray-900 dark:text-gray-100">
                  {new Date(createdKey.expiresAt).toLocaleDateString()}
                </span>
              </div>
            )}
          </div>

          <div className="flex justify-end">
            <Button onClick={handleClose} variant="primary">
              Done
            </Button>
          </div>
        </div>
      </Modal>
    );
  }

  // Show creation form
  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Create API Key">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 p-3">
            <div className="flex gap-2">
              <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0" />
              <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
            </div>
          </div>
        )}

        <Input
          label="Key Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Production API Key"
          required
          autoFocus
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Permissions
          </label>
          <div className="space-y-2">
            {['read', 'write', 'admin'].map((permission) => (
              <label
                key={permission}
                className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={permissions.includes(permission)}
                  onChange={() => handlePermissionToggle(permission)}
                  className="rounded border-gray-300 text-accent-blue focus:ring-accent-blue"
                />
                <div>
                  <div className="font-medium text-gray-900 dark:text-gray-100 capitalize">
                    {permission}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {permission === 'read' && 'View-only access to endpoints'}
                    {permission === 'write' && 'Read and modify access'}
                    {permission === 'admin' && 'Full access including webhooks and audit logs'}
                  </div>
                </div>
              </label>
            ))}
          </div>
        </div>

        <Input
          label="Expiration Date (Optional)"
          type="date"
          value={expiresAt}
          onChange={(e) => setExpiresAt(e.target.value)}
          min={new Date().toISOString().split('T')[0]}
        />

        <div className="flex gap-2 justify-end pt-2">
          <Button type="button" onClick={handleClose} variant="ghost">
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            loading={loading}
            disabled={!name.trim() || permissions.length === 0}
          >
            Create API Key
          </Button>
        </div>
      </form>
    </Modal>
  );
}

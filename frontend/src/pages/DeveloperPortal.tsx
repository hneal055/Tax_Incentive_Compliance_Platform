import { useState, useEffect } from 'react';
import { Plus, Key, AlertCircle, BookOpen, Code, Shield, Zap } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';
import CreateApiKeyModal from '../components/CreateApiKeyModal';
import ApiKeyCard from '../components/ApiKeyCard';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import TopBar from '../components/TopBar';
import api from '../api';
import type { ApiKey, ApiKeyCreated } from '../types';

export default function DeveloperPortal() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [rotatedKey, setRotatedKey] = useState<ApiKeyCreated | null>(null);
  const [copiedRotatedKey, setCopiedRotatedKey] = useState(false);

  useEffect(() => {
    loadApiKeys();
  }, []);

  const loadApiKeys = async () => {
    setLoading(true);
    setError('');
    try {
      const keys = await api.apiKeys.list();
      setApiKeys(keys);
    } catch (err: any) {
      console.error('Failed to load API keys:', err);
      setError(err?.response?.data?.detail || 'Failed to load API keys');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateApiKey = async (data: { name: string; permissions: string[]; expiresAt?: string }): Promise<ApiKeyCreated> => {
    const newKey = await api.apiKeys.create(data);
    await loadApiKeys();
    return newKey;
  };

  const handleDeleteApiKey = async (id: string) => {
    if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
      return;
    }

    try {
      await api.apiKeys.delete(id);
      await loadApiKeys();
    } catch (err: any) {
      console.error('Failed to delete API key:', err);
      alert(err?.response?.data?.detail || 'Failed to delete API key');
    }
  };

  const handleRotateApiKey = async (id: string) => {
    if (!confirm('Rotating this key will invalidate the current key immediately. Continue?')) {
      return;
    }

    try {
      const newKey = await api.apiKeys.rotate(id);
      setRotatedKey(newKey);
      await loadApiKeys();
    } catch (err: any) {
      console.error('Failed to rotate API key:', err);
      alert(err?.response?.data?.detail || 'Failed to rotate API key');
    }
  };

  const handleCopyRotatedKey = async () => {
    if (rotatedKey?.plaintext_key) {
      await navigator.clipboard.writeText(rotatedKey.plaintext_key);
      setCopiedRotatedKey(true);
      setTimeout(() => setCopiedRotatedKey(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-bg-primary pb-8">
      <TopBar title="Developer Portal" subtitle="Manage your API keys and access credentials" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        {/* Header Section */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              API Keys
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Create and manage API keys for programmatic access to PilotForge
            </p>
          </div>
          <Button
            variant="primary"
            icon={Plus}
            onClick={() => setShowCreateModal(true)}
          >
            Create API Key
          </Button>
        </div>

        {/* Rotated Key Alert */}
        {rotatedKey && (
          <div className="mb-6 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 p-4">
            <div className="flex gap-3">
              <Key className="h-5 w-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <h4 className="font-semibold text-green-900 dark:text-green-100">
                  API Key Rotated Successfully
                </h4>
                <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                  Your new API key is ready. Save it now - you won't be able to see it again!
                </p>
                <div className="mt-3 flex gap-2">
                  <input
                    type="text"
                    value={rotatedKey.plaintext_key}
                    readOnly
                    className="flex-1 px-3 py-2 border border-green-300 dark:border-green-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono text-sm"
                  />
                  <Button
                    onClick={handleCopyRotatedKey}
                    variant="outline"
                    size="sm"
                  >
                    {copiedRotatedKey ? 'Copied!' : 'Copy'}
                  </Button>
                  <Button
                    onClick={() => setRotatedKey(null)}
                    variant="ghost"
                    size="sm"
                  >
                    Dismiss
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Getting Started Guide */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card>
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
                <Key className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
                  Create API Key
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Generate a new API key to authenticate your requests
                </p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
                <Code className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
                  Use in Code
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Add the key to your request headers for authentication
                </p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100 dark:bg-green-900/30">
                <Shield className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
                  Stay Secure
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Rotate keys regularly and never share them publicly
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* API Keys List */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <Spinner size="lg" />
          </div>
        ) : error ? (
          <Card>
            <div className="flex gap-3 text-red-600 dark:text-red-400">
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <div>
                <h4 className="font-semibold">Error Loading API Keys</h4>
                <p className="text-sm mt-1">{error}</p>
                <Button
                  onClick={loadApiKeys}
                  variant="outline"
                  size="sm"
                  className="mt-3"
                >
                  Retry
                </Button>
              </div>
            </div>
          </Card>
        ) : apiKeys.length === 0 ? (
          <EmptyState
            icon={Key}
            title="No API keys yet"
            description="Create your first API key to get started with the PilotForge API"
            actionLabel="Create Your First API Key"
            onAction={() => setShowCreateModal(true)}
          />
        ) : (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Your API Keys ({apiKeys.length})
            </h2>
            <div className="grid gap-4">
              {apiKeys.map((key) => (
                <ApiKeyCard
                  key={key.id}
                  apiKey={key}
                  onDelete={handleDeleteApiKey}
                  onRotate={handleRotateApiKey}
                />
              ))}
            </div>
          </div>
        )}

        {/* Documentation Section */}
        <Card className="mt-8">
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-100 dark:bg-indigo-900/30">
              <BookOpen className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                API Documentation
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Learn how to integrate PilotForge into your applications with our comprehensive API documentation.
              </p>
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 font-mono text-sm">
                <div className="text-gray-600 dark:text-gray-400">Example request:</div>
                <pre className="mt-2 text-gray-900 dark:text-gray-100">
{`curl -X GET "http://localhost:8000/api/v1/productions/" \\
  -H "X-API-Key: your_api_key_here"`}
                </pre>
              </div>
              <div className="mt-4 flex gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open('http://localhost:8000/docs', '_blank')}
                >
                  View API Docs
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => window.open('http://localhost:8000/redoc', '_blank')}
                >
                  View ReDoc
                </Button>
              </div>
            </div>
          </div>
        </Card>

        {/* Best Practices */}
        <div className="mt-8 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 p-6">
          <div className="flex gap-3">
            <Zap className="h-5 w-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                Security Best Practices
              </h4>
              <ul className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
                <li className="flex items-start gap-2">
                  <span className="font-bold mt-0.5">•</span>
                  <span>Never commit API keys to version control or share them publicly</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold mt-0.5">•</span>
                  <span>Use environment variables to store API keys in your applications</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold mt-0.5">•</span>
                  <span>Rotate keys regularly and immediately if you suspect they've been compromised</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold mt-0.5">•</span>
                  <span>Use the minimum required permissions for each API key</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold mt-0.5">•</span>
                  <span>Set expiration dates for keys that don't need indefinite access</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      <CreateApiKeyModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreateApiKey}
      />
    </div>
  );
}

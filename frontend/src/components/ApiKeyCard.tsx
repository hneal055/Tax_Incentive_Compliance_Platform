import { useState } from 'react';
import { Key, Trash2, RefreshCw, Copy, Check, Calendar, Shield, Clock } from 'lucide-react';
import Button from './Button';
import type { ApiKey } from '../types';

interface ApiKeyCardProps {
  apiKey: ApiKey;
  onDelete: (id: string) => void;
  onRotate: (id: string) => void;
}

export default function ApiKeyCard({ apiKey, onDelete, onRotate }: ApiKeyCardProps) {
  const [showActions, setShowActions] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopyPrefix = async () => {
    await navigator.clipboard.writeText(apiKey.prefix);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isExpired = apiKey.expiresAt && new Date(apiKey.expiresAt) < new Date();
  const isExpiringSoon = apiKey.expiresAt && !isExpired && 
    new Date(apiKey.expiresAt) < new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);

  return (
    <div
      className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow"
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
              <Key className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                {apiKey.name}
              </h3>
              <div className="flex items-center gap-2 mt-1">
                <code className="text-xs font-mono text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-900 px-2 py-0.5 rounded">
                  {apiKey.prefix}...
                </code>
                <button
                  onClick={handleCopyPrefix}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  title="Copy prefix"
                >
                  {copied ? (
                    <Check className="h-3 w-3 text-green-600" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </button>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <Shield className="h-4 w-4 text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">Permissions:</span>
              <div className="flex gap-1">
                {apiKey.permissions.map((perm) => (
                  <span
                    key={perm}
                    className="px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-medium"
                  >
                    {perm}
                  </span>
                ))}
              </div>
            </div>

            {apiKey.lastUsedAt && (
              <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                <Clock className="h-4 w-4 text-gray-400" />
                <span>Last used: {new Date(apiKey.lastUsedAt).toLocaleDateString()}</span>
              </div>
            )}

            {apiKey.expiresAt && (
              <div className="flex items-center gap-2 text-sm">
                <Calendar className="h-4 w-4 text-gray-400" />
                <span className="text-gray-600 dark:text-gray-400">Expires:</span>
                <span
                  className={`font-medium ${
                    isExpired
                      ? 'text-red-600 dark:text-red-400'
                      : isExpiringSoon
                      ? 'text-yellow-600 dark:text-yellow-400'
                      : 'text-gray-900 dark:text-gray-100'
                  }`}
                >
                  {new Date(apiKey.expiresAt).toLocaleDateString()}
                  {isExpired && ' (Expired)'}
                  {isExpiringSoon && ' (Expiring soon)'}
                </span>
              </div>
            )}

            <div className="text-xs text-gray-500 dark:text-gray-400">
              Created {new Date(apiKey.createdAt).toLocaleDateString()}
            </div>
          </div>
        </div>

        <div
          className={`flex gap-2 transition-opacity duration-200 ${
            showActions ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <Button
            variant="outline"
            size="sm"
            icon={RefreshCw}
            onClick={() => onRotate(apiKey.id)}
            title="Rotate key"
          >
            Rotate
          </Button>
          <Button
            variant="danger"
            size="sm"
            icon={Trash2}
            onClick={() => onDelete(apiKey.id)}
            title="Delete key"
          >
            Delete
          </Button>
        </div>
      </div>

      {isExpired && (
        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg">
          <p className="text-sm text-red-700 dark:text-red-300">
            This API key has expired and can no longer be used. Please rotate or delete it.
          </p>
        </div>
      )}

      {isExpiringSoon && !isExpired && (
        <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg">
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            This API key will expire soon. Consider rotating it to avoid service interruptions.
          </p>
        </div>
      )}
    </div>
  );
}

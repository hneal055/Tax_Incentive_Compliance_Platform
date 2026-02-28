import { Zap } from 'lucide-react';
import Card from './Card';

function AIAdvisor() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-[28px] font-bold text-slate-900 tracking-tight">
          AI Advisor
        </h1>
        <p className="text-slate-500 mt-1.5 text-[15px]">
          Get intelligent recommendations for maximizing tax incentives.
        </p>
      </div>

      <Card title="Coming Soon" className="text-center py-16">
        <Zap className="w-16 h-16 text-blue-600 dark:text-blue-400 mx-auto mb-4 opacity-50" />
        <p className="text-slate-600 dark:text-slate-400 font-medium">
          AI-powered tax incentive recommendations
        </p>
        <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">
          Advanced features coming in the next release.
        </p>
      </Card>
    </div>
  );
}

export default AIAdvisor;

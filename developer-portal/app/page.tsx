import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center py-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🎬 PilotForge Developer Portal
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Tax Incentive Intelligence for Film & TV Productions
          </p>
          <p className="text-lg text-gray-500 mb-8">
            API documentation and integration guides for developers
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/docs"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-md"
            >
              View API Documentation
            </Link>
            <Link
              href="/docs/redoc"
              className="px-6 py-3 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors shadow-md"
            >
              ReDoc Documentation
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">🌍</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              32 Global Jurisdictions
            </h3>
            <p className="text-gray-600">
              Compare tax incentives across USA, Canada, UK, and more with our comprehensive API.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Tax Calculator API
            </h3>
            <p className="text-gray-600">
              Instant credit estimates with compliance checks and detailed breakdowns.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">📄</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Report Generation
            </h3>
            <p className="text-gray-600">
              Generate professional PDF and Excel reports programmatically.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Production Management
            </h3>
            <p className="text-gray-600">
              Track productions, budgets, and locations with RESTful endpoints.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Secure & Type-Safe
            </h3>
            <p className="text-gray-600">
              Built with FastAPI, featuring automatic validation and OpenAPI 3.1 spec.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Fast & Reliable
            </h3>
            <p className="text-gray-600">
              High-performance async API with comprehensive test coverage (127 tests).
            </p>
          </div>
        </div>

        {/* Quick Start Section */}
        <div className="mt-16 bg-white rounded-lg shadow-md p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Quick Start</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                1. API Base URL
              </h3>
              <div className="bg-gray-100 p-4 rounded-md font-mono text-sm">
                http://localhost:8000/api/v1
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                2. Example Request
              </h3>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-md font-mono text-sm overflow-x-auto">
                <pre>{`# Get all jurisdictions
curl http://localhost:8000/api/v1/jurisdictions

# Calculate tax incentive
curl -X POST http://localhost:8000/api/v1/calculator/calculate \\
  -H "Content-Type: application/json" \\
  -d '{
    "jurisdiction_id": "uuid-here",
    "total_budget": 5000000,
    "qualifying_spend": 4000000
  }'`}</pre>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                3. Explore the API
              </h3>
              <p className="text-gray-600 mb-4">
                Visit the interactive API documentation to try out endpoints:
              </p>
              <div className="flex gap-4">
                <Link
                  href="/docs"
                  className="px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
                >
                  Swagger UI →
                </Link>
                <Link
                  href="/docs/redoc"
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                >
                  ReDoc →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Resources Section */}
        <div className="mt-16 bg-blue-50 rounded-lg shadow-md p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Resources</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                📚 Documentation
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• <Link href="/docs" className="text-blue-600 hover:underline">Interactive API Docs (Swagger)</Link></li>
                <li>• <Link href="/docs/redoc" className="text-blue-600 hover:underline">ReDoc Documentation</Link></li>
                <li>• <a href="http://localhost:8000/openapi.json" className="text-blue-600 hover:underline">OpenAPI Specification</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                🔧 Developer Tools
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline">Backend Swagger UI</a></li>
                <li>• <a href="http://localhost:8000/redoc" className="text-blue-600 hover:underline">Backend ReDoc</a></li>
                <li>• <a href="http://localhost:8000/health" className="text-blue-600 hover:underline">API Health Check</a></li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            © 2025-2026 PilotForge - Tax Incentive Intelligence for Film & TV
          </p>
          <p className="text-gray-500 text-sm mt-2">
            Powered by FastAPI, React, and Next.js
          </p>
        </div>
      </footer>
    </div>
  );
}

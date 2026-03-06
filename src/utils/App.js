import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

function App() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <Topbar />
        <div className="flex-1 overflow-y-auto p-8">
          {/* Dashboard cards, charts, etc. go here */}
        </div>
      </main>
    </div>
  );
}

export default App;
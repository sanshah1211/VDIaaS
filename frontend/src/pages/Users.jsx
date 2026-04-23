import Dashboard from "../components/Layout/Dashboard"

export default function Users() {
  return (
    <Dashboard>
      <h1 className="text-2xl font-bold">Users Page</h1>
      <p>This content is coming from another page.</p>

      <div className="mt-4 p-4 bg-gray-200 rounded">
        Any React component or HTML can go here
      </div>
    </Dashboard>
  )
}
export function AuthLayout({ children }) {
  return (
    <main className="flex min-h-screen flex-col p-20 pr-5 pl-5 pt-36 pb-20">
      <div className="flex h-155 w-125 items-center justify-center p-6 lg:rounded-lg lg:bg-white lg:p-10 lg:shadow-xs lg:ring-1 lg:ring-zinc-950/5 dark:lg:bg-zinc-900 dark:lg:ring-white/10">
        {children}
      </div>
    </main>
  )
}

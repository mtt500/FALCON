// components/ui/spinner.tsx
export const Spinner = ({ className }: { className?: string }) => (
    <div
      className={`border-t-4 border-purple-600 border-solid rounded-full h-16 w-16 animate-spin ${className}`}
      style={{ borderTopColor: 'transparent' }}
    ></div>
  )
  
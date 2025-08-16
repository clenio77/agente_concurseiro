import React from 'react'
import { cn } from '../../lib/utils/cn'

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string
  error?: string | undefined
  helperText?: string
}

export const Checkbox: React.FC<CheckboxProps> = ({
  label,
  error,
  helperText,
  className,
  id,
  ...props
}) => {
  const checkboxId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`

  return (
    <div className="flex items-start">
      <div className="flex items-center h-5">
        <input
          id={checkboxId}
          type="checkbox"
          className={cn(
            'h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500',
            'dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-primary-400',
            error && 'border-red-500 focus:ring-red-500',
            className
          )}
          {...props}
        />
      </div>
      
      <div className="ml-3 text-sm">
        {label && (
          <label 
            htmlFor={checkboxId}
            className="font-medium text-gray-700 dark:text-gray-300 cursor-pointer"
          >
            {label}
          </label>
        )}
        
        {helperText && !error && (
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            {helperText}
          </p>
        )}
        
        {error && (
          <p className="text-red-600 dark:text-red-400 mt-1">
            {error}
          </p>
        )}
      </div>
    </div>
  )
}

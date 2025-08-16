import React from 'react'
import { cn } from '@/lib/utils/cn'

interface RadioOption {
  value: string
  label: string
  disabled?: boolean
}

interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> {
  label?: string
  options: RadioOption[]
  error?: string
  helperText?: string
  onChange?: (value: string) => void
}

export const Radio: React.FC<RadioProps> = ({
  label,
  options,
  error,
  helperText,
  onChange,
  className,
  name,
  ...props
}) => {
  const radioName = name || `radio-${Math.random().toString(36).substr(2, 9)}`

  const handleChange = (value: string) => {
    if (onChange) {
      onChange(value)
    }
  }

  return (
    <div className="w-full">
      {label && (
        <div className="mb-3">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {label}
          </label>
        </div>
      )}
      
      <div className="space-y-2">
        {options.map((option) => (
          <div key={option.value} className="flex items-center">
            <input
              id={`${radioName}-${option.value}`}
              name={radioName}
              type="radio"
              value={option.value}
              disabled={option.disabled}
              onChange={() => handleChange(option.value)}
              className={cn(
                'h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500',
                'dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-primary-400',
                error && 'border-red-500 focus:ring-red-500',
                option.disabled && 'opacity-50 cursor-not-allowed',
                className
              )}
              {...props}
            />
            
            <label 
              htmlFor={`${radioName}-${option.value}`}
              className={cn(
                'ml-3 text-sm font-medium text-gray-700 dark:text-gray-300',
                option.disabled && 'opacity-50 cursor-not-allowed',
                !option.disabled && 'cursor-pointer'
              )}
            >
              {option.label}
            </label>
          </div>
        ))}
      </div>
      
      {error && (
        <p className="mt-2 text-sm text-red-600 dark:text-red-400">
          {error}
        </p>
      )}
      
      {helperText && !error && (
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          {helperText}
        </p>
      )}
    </div>
  )
}

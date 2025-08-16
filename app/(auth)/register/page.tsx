'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Checkbox } from '@/components/ui/Checkbox'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card'
import { BookOpen, Eye, EyeOff, User, Mail, Lock } from 'lucide-react'

const studyLevels = [
  { value: 'iniciante', label: 'Iniciante' },
  { value: 'intermediario', label: 'Intermediário' },
  { value: 'avancado', label: 'Avançado' },
  { value: 'expert', label: 'Expert' }
]

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    studyLevel: '',
    agreeToTerms: false
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  
  const router = useRouter()

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Nome completo é obrigatório'
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email inválido'
    }

    if (!formData.password) {
      newErrors.password = 'Senha é obrigatória'
    } else if (formData.password.length < 6) {
      newErrors.password = 'Senha deve ter pelo menos 6 caracteres'
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Senhas não coincidem'
    }

    if (!formData.studyLevel) {
      newErrors.studyLevel = 'Nível de estudo é obrigatório'
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'Você deve aceitar os termos'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      // Simular criação de usuário (será substituído por Supabase)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Redirecionar para login
      router.push('/login?message=Conta criada com sucesso!')
    } catch (error) {
      setErrors({ general: 'Erro ao criar conta. Tente novamente.' })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Limpar erro do campo quando usuário começa a digitar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-600 to-primary-400 rounded-2xl mb-4">
            <BookOpen className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Agente Concurseiro
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Crie sua conta e comece a estudar
          </p>
        </div>

        {/* Register Form */}
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-xl">Criar Conta</CardTitle>
          </CardHeader>
          
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <Input
                label="Nome Completo"
                value={formData.fullName}
                onChange={(e) => handleInputChange('fullName', e.target.value)}
                placeholder="Seu nome completo"
                leftIcon={<User className="h-4 w-4" />}
                error={errors.fullName}
                required
              />
              
              <Input
                label="Email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="seu@email.com"
                leftIcon={<Mail className="h-4 w-4" />}
                error={errors.email}
                required
              />
              
              <Input
                label="Senha"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                placeholder="Sua senha"
                leftIcon={<Lock className="h-4 w-4" />}
                rightIcon={
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                }
                error={errors.password}
                required
              />
              
              <Input
                label="Confirmar Senha"
                type={showConfirmPassword ? 'text' : 'password'}
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                placeholder="Confirme sua senha"
                leftIcon={<Lock className="h-4 w-4" />}
                rightIcon={
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                }
                error={errors.confirmPassword}
                required
              />
              
              <Select
                label="Nível de Estudo"
                options={studyLevels}
                value={formData.studyLevel}
                onChange={(value) => handleInputChange('studyLevel', value)}
                placeholder="Selecione seu nível"
                error={errors.studyLevel}
                required
              />
              
              <Checkbox
                label="Concordo com os termos de uso e política de privacidade"
                checked={formData.agreeToTerms}
                onChange={(e) => handleInputChange('agreeToTerms', e.target.checked)}
                error={errors.agreeToTerms}
              />

              {errors.general && (
                <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                  {errors.general}
                </div>
              )}
            </CardContent>

            <CardFooter className="flex flex-col space-y-3">
              <Button 
                type="submit" 
                className="w-full" 
                loading={loading}
                disabled={loading}
              >
                {loading ? 'Criando conta...' : 'Criar Conta'}
              </Button>
              
              <div className="text-center text-sm text-gray-600 dark:text-gray-400">
                Já tem uma conta?{' '}
                <Link 
                  href="/login" 
                  className="text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
                >
                  Faça login
                </Link>
              </div>
            </CardFooter>
          </form>
        </Card>
      </div>
    </div>
  )
}

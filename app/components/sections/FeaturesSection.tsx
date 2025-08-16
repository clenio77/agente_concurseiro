'use client'

import React from 'react'
import { 
  Brain, 
  Target, 
  Trophy, 
  BookOpen, 
  Zap, 
  Users, 
  BarChart3, 
  Mic, 
  Eye, 
  TrendingUp, 
  Smartphone, 
  Globe 
} from 'lucide-react'

const features = [
  {
    icon: Brain,
    title: 'IA Inteligente',
    description: 'Algoritmos avançados que se adaptam ao seu estilo de aprendizado e identificam suas áreas de melhoria.',
    color: 'primary'
  },
  {
    icon: Target,
    title: 'Foco Personalizado',
    description: 'Planos de estudo adaptativos que se concentram nas matérias onde você mais precisa melhorar.',
    color: 'secondary'
  },
  {
    icon: Trophy,
    title: 'Gamificação Avançada',
    description: 'Sistema de pontos, níveis e conquistas que mantém você motivado e engajado nos estudos.',
    color: 'success'
  },
  {
    icon: BookOpen,
    title: 'Conteúdo Inteligente',
    description: 'Materiais atualizados e organizados por dificuldade, com revisão espaçada para melhor retenção.',
    color: 'warning'
  },
  {
    icon: Zap,
    title: 'Performance Analytics',
    description: 'Métricas detalhadas do seu progresso com insights para otimizar sua estratégia de estudo.',
    color: 'error'
  },
  {
    icon: Users,
    title: 'Comunidade Ativa',
    description: 'Conecte-se com outros concurseiros, compartilhe experiências e participe de grupos de estudo.',
    color: 'gamification'
  },
  {
    icon: BarChart3,
    title: 'Análise Comportamental',
    description: 'Identifica seus padrões de estudo e oferece recomendações personalizadas para maximizar a produtividade.',
    color: 'ai'
  },
  {
    icon: Mic,
    title: 'Assistente de Voz',
    description: 'Controle a plataforma por comandos de voz e receba feedback auditivo durante os estudos.',
    color: 'ar'
  },
  {
    icon: Eye,
    title: 'Realidade Aumentada',
    description: 'Experiências imersivas de estudo com visualizações 3D e interações avançadas.',
    color: 'primary'
  },
  {
    icon: TrendingUp,
    title: 'Predição de Tendências',
    description: 'Análise de dados para prever temas que podem aparecer nos próximos concursos.',
    color: 'secondary'
  },
  {
    icon: Smartphone,
    title: 'App Mobile',
    description: 'Estude em qualquer lugar com nossa aplicação móvel sincronizada com a versão web.',
    color: 'success'
  },
  {
    icon: Globe,
    title: 'Multiplataforma',
    description: 'Acesso completo em desktop, tablet e mobile com sincronização em tempo real.',
    color: 'warning'
  }
]

const getColorClasses = (color: string) => {
  const colorMap: Record<string, string> = {
    primary: 'bg-primary-100 text-primary-600 dark:bg-primary-900 dark:text-primary-400',
    secondary: 'bg-secondary-100 text-secondary-600 dark:bg-secondary-900 dark:text-secondary-400',
    success: 'bg-success-100 text-success-600 dark:bg-success-900 dark:text-success-400',
    warning: 'bg-warning-100 text-warning-600 dark:bg-warning-900 dark:text-warning-400',
    error: 'bg-error-100 text-error-600 dark:bg-error-900 dark:text-error-400',
    gamification: 'bg-gamification-100 text-gamification-600 dark:bg-gamification-900 dark:text-gamification-400',
    ai: 'bg-ai-100 text-ai-600 dark:bg-ai-900 dark:text-ai-400',
    ar: 'bg-ar-100 text-ar-600 dark:bg-ar-900 dark:text-ar-400'
  }
  return colorMap[color] || colorMap.primary
}

export default function FeaturesSection() {
  return (
    <section className="py-24 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Recursos Revolucionários para{' '}
            <span className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
              Concurseiros
            </span>
          </h2>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Nossa plataforma combina as mais avançadas tecnologias de IA, gamificação e análise comportamental 
            para transformar sua preparação para concursos.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600"
            >
              {/* Icon */}
              <div className={`w-16 h-16 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200 ${getColorClasses(feature.color)}`}>
                <feature.icon className="w-8 h-8" />
              </div>

              {/* Content */}
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                {feature.description}
              </p>

              {/* Hover Effect */}
              <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <div className="w-full h-1 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"></div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <div className="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-2xl p-8 border border-primary-200 dark:border-primary-800">
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Pronto para Transformar seus Estudos?
            </h3>
            <p className="text-lg text-gray-600 dark:text-gray-400 mb-6 max-w-2xl mx-auto">
              Junte-se a milhares de concurseiros que já estão usando nossa plataforma para alcançar a aprovação.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors duration-200 shadow-lg hover:shadow-xl">
                Começar Gratuitamente
              </button>
              <button className="border-2 border-primary-600 text-primary-600 hover:bg-primary-600 hover:text-white px-8 py-3 rounded-lg font-semibold transition-all duration-200">
                Ver Planos Premium
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

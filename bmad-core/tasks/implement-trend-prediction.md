# Implementar Sistema de Predição de Tendências

## Objetivo
Implementar um sistema completo de predição de tendências para o mercado brasileiro de concursos públicos, utilizando big data, machine learning e market intelligence para maximizar as chances de aprovação dos candidatos.

## Pré-requisitos
- Pipeline de dados robusto implementado
- Machine learning infrastructure setup
- Conhecimento do mercado brasileiro de concursos
- APIs e web scraping capabilities

## Contexto Técnico
O sistema de predição de tendências utilizará múltiplas fontes de dados, processamento em tempo real, e modelos de ML para gerar insights estratégicos sobre o mercado de concursos. O foco é fornecer vantagem competitiva através de inteligência de mercado acionável.

## Fases de Implementação

### Fase 1: Data Infrastructure (Semanas 1-2)

#### Data Pipeline Architecture
```python
# data_pipeline.py
class ConcursoDataPipeline:
    def __init__(self):
        self.scrapers = {
            'dou': DOUWebScraper(),
            'pncp': PNCPAPIScraper(),
            'cespe': CESPEScraper(),
            'fcc': FCCScraper(),
            'vunesp': VUNESPScraper()
        }
        self.processors = {
            'text': TextProcessor(),
            'dates': DateProcessor(),
            'locations': LocationProcessor()
        }
        self.storage = DataStorage()
    
    def run_daily_collection(self):
        """Execute daily data collection pipeline"""
        for source, scraper in self.scrapers.items():
            try:
                raw_data = scraper.collect_daily_data()
                processed_data = self.process_data(raw_data, source)
                self.storage.store_processed_data(processed_data, source)
            except Exception as e:
                self.log_error(f"Error in {source}: {e}")
    
    def process_data(self, raw_data, source):
        """Process raw data for ML consumption"""
        pass
```

#### Web Scraping Setup
```python
# scrapers/dou_scraper.py
import scrapy
from scrapy.crawler import CrawlerProcess

class DOUEditalSpider(scrapy.Spider):
    name = 'dou_editais'
    start_urls = ['https://www.in.gov.br/consulta/-/buscar/dou']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_search_page,
                meta={'search_term': 'concurso público'}
            )
    
    def parse_search_page(self, response):
        editals = response.css('div.resultado-busca')
        for edital in editals:
            yield {
                'source': 'dou',
                'title': edital.css('h3 a::text').get(),
                'organ': self.extract_organ(edital),
                'publication_date': self.extract_date(edital),
                'url': edital.css('h3 a::attr(href)').get(),
                'content': self.extract_content(edital),
                'extracted_at': datetime.now()
            }
    
    def extract_organ(self, edital):
        """Extract organ name from edital"""
        pass
    
    def extract_date(self, edital):
        """Extract publication date"""
        pass
```

#### Data Storage Schema
```python
# models/market_data.py
class EditalData(Base):
    __tablename__ = "edital_data"
    
    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)  # dou, cespe, fcc, etc.
    
    # Basic Information
    title = Column(Text, nullable=False)
    organ = Column(String, nullable=False)
    banca = Column(String)
    publication_date = Column(Date, nullable=False)
    
    # Opportunity Data
    num_vagas = Column(Integer)
    salary_min = Column(Float)
    salary_max = Column(Float)
    location_city = Column(String)
    location_state = Column(String)
    
    # Content Analysis
    content_raw = Column(Text)
    content_processed = Column(JSON)
    topics_identified = Column(JSON)
    
    # Predictions
    predicted_competition_level = Column(Float)
    predicted_approval_difficulty = Column(Float)
    opportunity_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MarketTrend(Base):
    __tablename__ = "market_trends"
    
    id = Column(Integer, primary_key=True)
    trend_type = Column(String, nullable=False)  # timing, content, market
    
    # Trend Data
    trend_name = Column(String, nullable=False)
    trend_value = Column(Float)
    confidence_score = Column(Float)
    
    # Context
    sector = Column(String)
    geographic_scope = Column(String)
    time_horizon = Column(String)  # short, medium, long
    
    # Metadata
    first_detected = Column(Date)
    last_validated = Column(Date)
    status = Column(String, default='active')  # active, declining, obsolete
```

#### Tasks da Fase 1:
- [ ] **Setup Web Scraping Infrastructure**
  - Scrapy spiders para principais fontes
  - Rate limiting e ethical scraping
  - Error handling e retry logic
  - Data validation e cleaning

- [ ] **Implementar API Integrations**
  ```python
  # api_clients/government_apis.py
  class PNCPAPIClient:
      def __init__(self, api_key):
          self.api_key = api_key
          self.base_url = "https://pncp.gov.br/api"
      
      def get_recent_editals(self, days_back=30):
          """Fetch recent editals from PNCP"""
          pass
      
      def search_editals(self, filters):
          """Search editals with specific filters"""
          pass
  ```

- [ ] **Create Data Processing Pipeline**
  - Text preprocessing para editais
  - Entity extraction (órgãos, cargos, salários)
  - Date normalization
  - Geographic standardization

- [ ] **Setup Data Storage Infrastructure**
  - PostgreSQL optimization para time-series data
  - Indexing strategy para fast queries
  - Data retention policies
  - Backup e recovery procedures

### Fase 2: Basic ML Models (Semanas 3-4)

#### Time Series Forecasting
```python
# models/forecasting.py
from prophet import Prophet
import pandas as pd

class EditalTimingPredictor:
    def __init__(self):
        self.models = {}  # One model per organ/banca
        self.trained = False
    
    def prepare_training_data(self, historical_editals):
        """Prepare data for Prophet model"""
        df = pd.DataFrame({
            'ds': historical_editals['publication_date'],
            'y': 1,  # Binary: edital published or not
            'organ': historical_editals['organ'],
            'banca': historical_editals['banca']
        })
        
        # Aggregate by week
        weekly_data = df.groupby(['ds', 'organ']).agg({
            'y': 'sum'
        }).reset_index()
        
        return weekly_data
    
    def train_models(self, training_data):
        """Train Prophet models for each organ"""
        for organ in training_data['organ'].unique():
            organ_data = training_data[training_data['organ'] == organ][['ds', 'y']]
            
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False
            )
            
            model.fit(organ_data)
            self.models[organ] = model
        
        self.trained = True
    
    def predict_next_editals(self, organ, months_ahead=12):
        """Predict when next editals will be published"""
        if not self.trained or organ not in self.models:
            raise ValueError(f"Model not trained for organ: {organ}")
        
        model = self.models[organ]
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=months_ahead*4, freq='W')
        forecast = model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(months_ahead*4)
```

#### Content Analysis Models
```python
# models/content_analysis.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy

class EditalContentAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('pt_core_news_sm')
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='portuguese',
            ngram_range=(1, 3)
        )
        self.topic_model = LatentDirichletAllocation(
            n_components=50,
            random_state=42
        )
    
    def analyze_content_trends(self, edital_texts):
        """Analyze trending topics in editals"""
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in edital_texts]
        
        # Vectorize
        doc_term_matrix = self.vectorizer.fit_transform(processed_texts)
        
        # Topic modeling
        self.topic_model.fit(doc_term_matrix)
        
        # Extract trending topics
        feature_names = self.vectorizer.get_feature_names_out()
        trending_topics = []
        
        for topic_idx, topic in enumerate(self.topic_model.components_):
            top_words = [feature_names[i] for i in topic.argsort()[-10:]]
            trending_topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weight': topic.max(),
                'trend_score': self.calculate_trend_score(topic)
            })
        
        return sorted(trending_topics, key=lambda x: x['trend_score'], reverse=True)
    
    def preprocess_text(self, text):
        """Preprocess edital text"""
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc 
                 if not token.is_stop and not token.is_punct and token.is_alpha]
        return ' '.join(tokens)
    
    def calculate_trend_score(self, topic_distribution):
        """Calculate trending score for topic"""
        # Implementation specific to trend calculation
        pass
```

#### Tasks da Fase 2:
- [ ] **Implementar Time Series Models**
  - Prophet models para timing prediction
  - ARIMA models para comparison
  - Seasonal decomposition analysis
  - Model validation e backtesting

- [ ] **Criar Content Analysis Pipeline**
  - NLP preprocessing em português
  - Topic modeling com LDA
  - Trend detection algorithms
  - Sentiment analysis integration

- [ ] **Desenvolver Opportunity Scoring**
  ```python
  class OpportunityScorer:
      def calculate_opportunity_score(self, edital_data):
          factors = {
              'competition_level': self.estimate_competition(edital_data),
              'salary_attractiveness': self.score_salary(edital_data),
              'location_desirability': self.score_location(edital_data),
              'career_progression': self.score_career_potential(edital_data),
              'timing_advantage': self.score_timing(edital_data)
          }
          
          # Weighted combination
          weights = {
              'competition_level': 0.3,
              'salary_attractiveness': 0.25,
              'location_desirability': 0.2,
              'career_progression': 0.15,
              'timing_advantage': 0.1
          }
          
          score = sum(factors[f] * weights[f] for f in factors)
          return {
              'total_score': score,
              'factors': factors,
              'recommendation': self.generate_recommendation(score)
          }
  ```

- [ ] **Setup Model Evaluation Framework**
  - Accuracy metrics tracking
  - Prediction confidence scoring
  - Model performance monitoring
  - A/B testing infrastructure

### Fase 3: Advanced Analytics (Semanas 5-6)

#### Market Intelligence Engine
```python
# intelligence/market_analyzer.py
class MarketIntelligenceEngine:
    def __init__(self):
        self.data_aggregator = DataAggregator()
        self.trend_detector = TrendDetector()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.economic_correlator = EconomicCorrelator()
    
    def generate_market_report(self, time_horizon='6_months'):
        """Generate comprehensive market intelligence report"""
        report = {
            'executive_summary': self.create_executive_summary(),
            'sector_analysis': self.analyze_sectors(),
            'geographic_opportunities': self.analyze_geographic_trends(),
            'timing_predictions': self.predict_timing_patterns(),
            'emerging_trends': self.identify_emerging_trends(),
            'risk_assessment': self.assess_market_risks(),
            'recommendations': self.generate_strategic_recommendations()
        }
        
        return report
    
    def analyze_sectors(self):
        """Analyze opportunities by government sector"""
        sectors = ['executivo', 'judiciario', 'legislativo', 'mp', 'tribunais']
        analysis = {}
        
        for sector in sectors:
            sector_data = self.data_aggregator.get_sector_data(sector)
            analysis[sector] = {
                'growth_rate': self.calculate_growth_rate(sector_data),
                'competition_level': self.assess_competition(sector_data),
                'salary_trends': self.analyze_salary_trends(sector_data),
                'opportunity_forecast': self.forecast_opportunities(sector_data)
            }
        
        return analysis
```

#### Competitive Intelligence
```python
# intelligence/competitive_analyzer.py
class CompetitiveAnalyzer:
    def __init__(self):
        self.banca_patterns = BancaPatternAnalyzer()
        self.market_segmentation = MarketSegmentationAnalyzer()
        self.opportunity_mapper = OpportunityMapper()
    
    def analyze_competitive_landscape(self):
        """Analyze competitive dynamics in concursos market"""
        analysis = {
            'banca_preferences': self.analyze_banca_preferences(),
            'niche_opportunities': self.identify_niche_opportunities(),
            'market_saturation': self.assess_market_saturation(),
            'strategic_gaps': self.identify_strategic_gaps()
        }
        
        return analysis
    
    def identify_niche_opportunities(self):
        """Identify underserved niches with high opportunity"""
        # Analysis of low-competition, high-value opportunities
        pass
    
    def analyze_banca_preferences(self):
        """Analyze each banca's patterns and preferences"""
        bancas = ['cespe', 'fcc', 'vunesp', 'fgv', 'ibfc']
        preferences = {}
        
        for banca in bancas:
            preferences[banca] = {
                'content_preferences': self.analyze_content_patterns(banca),
                'difficulty_patterns': self.analyze_difficulty_trends(banca),
                'geographic_focus': self.analyze_geographic_patterns(banca),
                'timing_patterns': self.analyze_timing_patterns(banca)
            }
        
        return preferences
```

#### Tasks da Fase 3:
- [ ] **Implementar Advanced ML Models**
  - Ensemble methods para predições
  - Deep learning para pattern recognition
  - Graph neural networks para relationship analysis
  - Reinforcement learning para optimization

- [ ] **Criar Market Intelligence Dashboard**
  ```python
  def render_market_intelligence_dashboard():
      st.title("🔮 Market Intelligence - Concursos")
      
      # Executive Summary
      with st.container():
          st.subheader("📊 Visão Executiva")
          col1, col2, col3, col4 = st.columns(4)
          
          with col1:
              st.metric("Editais Previstos (30d)", "127", "+23%")
          with col2:
              st.metric("Oportunidades Alto Valor", "15", "+5")
          with col3:
              st.metric("Competição Média", "1:45", "-8%")
          with col4:
              st.metric("Score Mercado", "8.7/10", "+0.3")
      
      # Trend Analysis
      st.subheader("📈 Análise de Tendências")
      # Implementation of interactive charts
  ```

- [ ] **Desenvolver Prediction Confidence System**
  - Uncertainty quantification
  - Confidence intervals
  - Risk assessment
  - Scenario analysis

- [ ] **Criar Alert System Avançado**
  - Real-time opportunity alerts
  - Market shift notifications
  - Personalized recommendations
  - Strategic timing alerts

### Fase 4: Personalization & Integration (Semanas 7-8)

#### Personalized Recommendation Engine
```python
# personalization/recommendation_engine.py
class PersonalizedRecommendationEngine:
    def __init__(self):
        self.user_profiler = UserProfiler()
        self.opportunity_matcher = OpportunityMatcher()
        self.career_planner = CareerPlanner()
    
    def generate_personalized_insights(self, user_id):
        """Generate personalized market insights for user"""
        user_profile = self.user_profiler.get_user_profile(user_id)
        
        recommendations = {
            'top_opportunities': self.rank_opportunities_for_user(user_profile),
            'study_prioritization': self.prioritize_study_topics(user_profile),
            'timing_strategy': self.optimize_timing_strategy(user_profile),
            'career_path': self.recommend_career_progression(user_profile)
        }
        
        return recommendations
    
    def rank_opportunities_for_user(self, user_profile):
        """Rank all current opportunities by fit with user profile"""
        all_opportunities = self.get_current_opportunities()
        
        ranked_opportunities = []
        for opportunity in all_opportunities:
            fit_score = self.calculate_user_opportunity_fit(user_profile, opportunity)
            ranked_opportunities.append({
                'opportunity': opportunity,
                'fit_score': fit_score,
                'reasoning': self.explain_fit_score(user_profile, opportunity, fit_score)
            })
        
        return sorted(ranked_opportunities, key=lambda x: x['fit_score'], reverse=True)
```

#### Integration com Study System
```python
# integration/study_optimization.py
class StudyOptimizationIntegrator:
    def __init__(self):
        self.trend_predictor = TrendPredictor()
        self.study_planner = StudyPlanner()
        self.content_prioritizer = ContentPrioritizer()
    
    def optimize_study_plan_with_trends(self, user_id, current_study_plan):
        """Optimize study plan based on market trends"""
        trends = self.trend_predictor.get_relevant_trends(user_id)
        
        optimized_plan = {
            'priority_subjects': self.prioritize_subjects_by_trends(trends),
            'content_focus': self.adjust_content_focus(trends),
            'timing_optimization': self.optimize_study_timing(trends),
            'resource_allocation': self.optimize_resource_allocation(trends)
        }
        
        return optimized_plan
    
    def adjust_gamification_based_on_trends(self, user_trends):
        """Adjust gamification system based on predicted trends"""
        # Achievement unlocks based on trend preparation
        # Bonus points for studying trending topics
        # Challenges aligned with market opportunities
        pass
```

#### Tasks da Fase 4:
- [ ] **Implementar User Profiling Avançado**
  - Career goals analysis
  - Learning pattern recognition
  - Risk tolerance assessment
  - Geographic preference modeling

- [ ] **Integrar com Sistema de Estudos**
  - Study plan optimization
  - Content prioritization
  - Resource allocation
  - Progress tracking enhancement

- [ ] **Criar Recommendation API**
  ```python
  # api/trend_recommendations.py
  @router.get("/trends/recommendations/{user_id}")
  async def get_personalized_recommendations(
      user_id: int,
      horizon: str = "6_months",
      risk_level: str = "medium"
  ):
      engine = PersonalizedRecommendationEngine()
      recommendations = engine.generate_personalized_insights(user_id)
      
      return {
          "user_id": user_id,
          "recommendations": recommendations,
          "generated_at": datetime.utcnow(),
          "confidence_score": recommendations.get("confidence", 0.85)
      }
  ```

- [ ] **Desenvolver Real-time Analytics**
  - Live market monitoring
  - Real-time trend detection
  - Instant opportunity alerts
  - Dynamic recommendation updates

## Critérios de Aceitação

### Technical Performance
- [ ] Data pipeline processes 10,000+ documents/day
- [ ] ML model accuracy > 80% for timing predictions
- [ ] Content analysis relevance > 75%
- [ ] API response time < 500ms
- [ ] System availability > 99.5%

### Business Value
- [ ] User engagement increase +30%
- [ ] Study efficiency improvement +25%
- [ ] Opportunity identification accuracy +40%
- [ ] User satisfaction with predictions > 4.0/5

### Data Quality
- [ ] Data freshness < 4 hours
- [ ] Source coverage > 95% of major editals
- [ ] Data accuracy > 95%
- [ ] Prediction confidence tracking implemented

## Integração com Sistema Existente

### Database Integration
```python
# Update existing models
class User(Base):
    # Add trend preference fields
    preferred_sectors = Column(JSON)
    geographic_preferences = Column(JSON)
    career_goals = Column(JSON)
    risk_tolerance = Column(String)

class StudyPlan(Base):
    # Add trend-based optimization
    trend_optimization_enabled = Column(Boolean, default=True)
    market_alignment_score = Column(Float)
    last_trend_update = Column(DateTime)
```

### API Extensions
```python
# New API endpoints
@router.get("/trends/market-overview")
async def get_market_overview():
    """Get current market overview and trends"""
    pass

@router.get("/trends/predictions/{user_id}")
async def get_user_predictions(user_id: int):
    """Get personalized predictions for user"""
    pass

@router.post("/trends/feedback")
async def submit_prediction_feedback(feedback: PredictionFeedback):
    """Submit feedback on prediction accuracy"""
    pass
```

## Testes Específicos

### Data Pipeline Testing
```python
def test_data_collection_accuracy():
    # Test scraper accuracy
    # Validate data cleaning
    # Check for missing fields
    pass

def test_ml_model_accuracy():
    # Backtesting on historical data
    # Cross-validation results
    # Prediction confidence validation
    pass
```

### Integration Testing
```python
def test_recommendation_integration():
    # Test with existing user data
    # Validate study plan integration
    # Check API response format
    pass
```

## Monitoring e Analytics

### System Monitoring
- Data pipeline health
- ML model performance
- Prediction accuracy tracking
- User engagement with predictions

### Business Monitoring  
- Market trend identification accuracy
- User satisfaction with recommendations
- Impact on study effectiveness
- ROI of prediction insights

## Documentação

### Technical Documentation
- [ ] Data pipeline architecture
- [ ] ML model specifications
- [ ] API documentation
- [ ] Deployment guide

### User Documentation
- [ ] Market intelligence guide
- [ ] How to interpret predictions
- [ ] Using recommendations effectively
- [ ] Trend analysis tutorials

## Entregáveis

1. **Data Pipeline Infrastructure** para coleta automatizada
2. **ML Models Suite** para predições temporais e de conteúdo
3. **Market Intelligence Engine** para análise competitiva
4. **Personalization System** para recomendações customizadas
5. **Interactive Dashboards** para visualização de insights
6. **Alert System** para oportunidades time-sensitive
7. **API Integration** com sistema existente
8. **Testing Framework** para validação contínua
9. **Documentation Package** completo
10. **Monitoring Dashboard** para system health

Este task deve resultar em um sistema de predição de tendências que fornece vantagem competitiva significativa aos candidatos através de market intelligence acionável.

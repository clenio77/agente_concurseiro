# Code Quality Checklist - Agente Concurseiro

## Visão Geral
Este checklist garante que todo código no projeto Agente Concurseiro atenda aos mais altos padrões de qualidade, maintainability e performance.

## 📋 Pre-Development Checklist

### Planning & Design
- [ ] **Requirements claramente definidos**
  - User story ou task bem especificada
  - Acceptance criteria detalhados
  - Edge cases identificados
  - Performance requirements estabelecidos

- [ ] **Design review concluído**
  - Arquitetura aprovada pelo Architect Agent
  - Integration points identificados
  - Database schema changes reviewados
  - API contracts definidos

- [ ] **Dependências identificadas**
  - Libraries necessárias listadas
  - Version compatibility verificada
  - Security vulnerabilities checked
  - License compatibility confirmed

## 🔧 Development Checklist

### Code Structure & Organization
- [ ] **File organization apropriada**
  - Código na estrutura de diretórios correta
  - Naming conventions seguidas consistentemente
  - Related functionality agrupada logicamente
  - Clear separation of concerns

- [ ] **Function & Class Design**
  - Single Responsibility Principle aplicado
  - Functions < 20 linhas (idealmente < 15)
  - Classes < 200 linhas (idealmente < 150)
  - Maximum 4 parameters por function
  - Descriptive naming sem abbreviations

- [ ] **Error Handling robusto**
  ```python
  # ✅ BOM
  try:
      result = ai_service.analyze_question(question)
      if not result.success:
          logger.warning(f"AI analysis failed: {result.error}")
          return fallback_analysis(question)
  except AIServiceError as e:
      logger.error(f"AI service unavailable: {e}")
      raise ServiceUnavailableError("Analysis temporarily unavailable")
  except Exception as e:
      logger.exception(f"Unexpected error in analysis: {e}")
      raise InternalServerError("Internal analysis error")
  
  # ❌ RUIM
  try:
      result = ai_service.analyze_question(question)
  except:
      pass
  ```

### Python Specific Standards
- [ ] **PEP 8 compliance**
  - Line length ≤ 88 characters (Black default)
  - Proper indentation (4 spaces)
  - Import organization (isort compatible)
  - Consistent use of quotes

- [ ] **Type hints obrigatórios**
  ```python
  # ✅ BOM
  def calculate_score(
      answers: List[str], 
      correct_answers: List[str],
      weights: Optional[List[float]] = None
  ) -> ScoreResult:
      """Calculate quiz score with weighted answers."""
      
  # ❌ RUIM
  def calculate_score(answers, correct_answers, weights=None):
  ```

- [ ] **Docstrings Google style**
  ```python
  # ✅ BOM
  def analyze_performance(
      user_id: int, 
      time_period: timedelta
  ) -> PerformanceAnalysis:
      """Analyze user performance over specified time period.
      
      Args:
          user_id: Unique identifier for the user
          time_period: Time period for analysis
          
      Returns:
          PerformanceAnalysis object with detailed metrics
          
      Raises:
          UserNotFoundError: If user_id doesn't exist
          InvalidTimeRangeError: If time_period is invalid
      """
  ```

### Performance Standards
- [ ] **Database optimization**
  - Queries use appropriate indexes
  - N+1 query problems avoided
  - Eager loading for relationships used appropriately
  - Pagination implemented for large datasets

- [ ] **Memory management**
  ```python
  # ✅ BOM - Context manager para resources
  async with database.transaction():
      results = await process_large_dataset(data)
  
  # ✅ BOM - Generator para large datasets
  def process_questions(question_ids: List[int]) -> Iterator[ProcessedQuestion]:
      for question_id in question_ids:
          yield process_single_question(question_id)
  
  # ❌ RUIM - Loading everything in memory
  all_questions = [process_question(id) for id in all_question_ids]
  ```

- [ ] **Async/await properly used**
  - I/O operations são async
  - CPU-bound tasks não bloqueiam event loop
  - Proper exception handling em async contexts

### Security Standards
- [ ] **Input validation rigorosa**
  ```python
  # ✅ BOM
  @router.post("/quiz/submit")
  async def submit_quiz(
      quiz_submission: QuizSubmission,  # Pydantic validation
      current_user: User = Depends(get_current_user)  # Auth required
  ):
      # Additional business logic validation
      if len(quiz_submission.answers) > MAX_ANSWERS:
          raise ValidationError("Too many answers provided")
  ```

- [ ] **No sensitive data em logs**
  ```python
  # ✅ BOM
  logger.info(f"User {user_id} submitted quiz {quiz_id}")
  
  # ❌ RUIM
  logger.info(f"User answered: {user_answers}")  # Might contain PII
  ```

- [ ] **SQL injection prevention**
  - Sempre usar parameterized queries
  - ORM utilizado corretamente
  - Dynamic SQL evitado

## 🧪 Testing Checklist

### Unit Tests
- [ ] **Coverage requirements met**
  - Minimum 90% coverage para código novo
  - Critical paths têm 100% coverage
  - Edge cases testados
  - Error conditions testadas

- [ ] **Test quality standards**
  ```python
  # ✅ BOM - Clear, specific test
  def test_quiz_score_calculation_with_weighted_answers():
      """Test that weighted answers are calculated correctly."""
      # Arrange
      answers = ["A", "B", "C"]
      correct = ["A", "B", "D"] 
      weights = [1.0, 2.0, 3.0]
      
      # Act
      result = calculate_quiz_score(answers, correct, weights)
      
      # Assert
      assert result.total_score == 3.0  # (1.0 + 2.0 + 0.0)
      assert result.weighted_score == 0.5  # 3.0 / 6.0
      assert result.correct_count == 2
  
  # ❌ RUIM - Vague test
  def test_scoring():
      result = calculate_quiz_score(["A"], ["A"])
      assert result.total_score > 0
  ```

### Integration Tests
- [ ] **API endpoints testados**
  - Happy path scenarios
  - Error scenarios (400, 401, 403, 404, 500)
  - Input validation
  - Authentication/authorization

- [ ] **Database interactions testadas**
  - CRUD operations
  - Transaction handling
  - Constraint violations
  - Concurrent access scenarios

### Educational Feature Tests
- [ ] **Gamification logic testada**
  - Achievement unlock conditions
  - Point calculation accuracy
  - Leaderboard ranking correctness
  - Streak calculation validation

- [ ] **AI integration testada**
  - Mock responses para consistency
  - Error handling quando AI services falham
  - Rate limiting respected
  - Cost optimization verified

## 📊 Performance Checklist

### Response Time Standards
- [ ] **API performance targets**
  - GET requests: < 200ms (95th percentile)
  - POST requests: < 500ms (95th percentile)
  - AI-powered requests: < 3s (95th percentile)
  - Database queries: < 100ms (95th percentile)

### Resource Usage
- [ ] **Memory efficiency**
  - Memory leaks identified e fixed
  - Large datasets handled via streaming/pagination
  - Caching implemented appropriately
  - Resource cleanup in finally blocks

- [ ] **Database performance**
  - Query execution plans reviewed
  - Indexes optimized
  - Connection pooling configured
  - Query caching implemented where appropriate

## 🔍 Code Review Checklist

### Before Submitting for Review
- [ ] **Self-review completed**
  - Code walkthrough performed
  - Comments added where necessary
  - Dead code removed
  - TODO comments justified or removed

- [ ] **Automated checks passed**
  - Linting (pylint, flake8) passa sem warnings
  - Type checking (mypy) passa
  - Security scanning (bandit) passa
  - Tests pass locally

### Review Criteria
- [ ] **Functionality verification**
  - Code does what it's supposed to do
  - Edge cases handled appropriately
  - Error scenarios managed gracefully
  - Performance requirements met

- [ ] **Maintainability assessment**
  - Code is readable e self-documenting
  - Complex logic explained with comments
  - Consistent with existing codebase
  - Future extensibility considered

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] **Environment configuration**
  - Environment variables properly set
  - Database migrations applied
  - Dependencies updated
  - Configuration validated

- [ ] **Monitoring setup**
  - Logging configuration verified
  - Error tracking enabled
  - Performance monitoring active
  - Health checks implemented

### Post-Deployment
- [ ] **Smoke tests**
  - Critical user journeys verified
  - API endpoints responding
  - Database connectivity confirmed
  - AI services integration working

- [ ] **Performance monitoring**
  - Response times within targets
  - Error rates < 0.1%
  - Memory usage stable
  - Database performance optimal

## 🎓 Educational System Specific Checks

### Learning Effectiveness
- [ ] **Educational features validated**
  - Spaced repetition algorithm accuracy
  - Adaptive difficulty working correctly
  - Progress tracking accurate
  - Personalization effective

### Data Privacy for Education
- [ ] **LGPD compliance para dados educacionais**
  - Student data protection implemented
  - Consent management working
  - Data anonymization when required
  - Right to deletion supported

### Accessibility
- [ ] **WCAG 2.1 AA compliance**
  - Screen reader compatibility
  - Keyboard navigation support
  - Color contrast requirements met
  - Alternative text para images

## ⚠️ Critical Issues (Never Accept)

### Security Vulnerabilities
- [ ] **Zero tolerance items**
  - Hardcoded credentials
  - SQL injection vulnerabilities
  - XSS vulnerabilities
  - Missing authentication checks
  - Sensitive data in logs
  - Unencrypted sensitive data transmission

### Performance Killers
- [ ] **Unacceptable patterns**
  - N+1 database queries
  - Blocking operations in async contexts
  - Memory leaks
  - Infinite loops or recursion
  - Missing pagination para large datasets

### Code Quality Issues
- [ ] **Anti-patterns to reject**
  - God objects (classes > 500 lines)
  - Functions > 50 lines
  - Circular dependencies
  - Magic numbers/strings
  - Dead code
  - Commented-out code in production

## 📝 Documentation Requirements

### Code Documentation
- [ ] **Inline documentation**
  - Public APIs fully documented
  - Complex algorithms explained
  - Business logic rationale provided
  - Performance considerations noted

### External Documentation
- [ ] **User-facing documentation**
  - API documentation updated
  - User guides current
  - Troubleshooting guides available
  - Performance characteristics documented

## ✅ Final Validation

### Quality Gates
- [ ] **All automated checks pass**
- [ ] **Manual testing completed**
- [ ] **Performance benchmarks met**
- [ ] **Security review passed**
- [ ] **Educational effectiveness validated**
- [ ] **Accessibility requirements met**
- [ ] **Documentation complete**

### Sign-off Required
- [ ] **Developer self-review ✓**
- [ ] **Peer code review ✓**
- [ ] **QA testing ✓**
- [ ] **Product owner approval ✓**
- [ ] **Security review ✓** (for security-sensitive changes)

---

**Remember**: Quality is not negotiable. Code that doesn't meet these standards should not be merged into main branch. When in doubt, err on the side of higher quality standards.

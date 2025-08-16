# Security & Privacy Checklist - Agente Concurseiro

## Visão Geral
Checklist abrangente para garantir máxima segurança e proteção de privacidade no Agente Concurseiro, com foco especial em dados educacionais e compliance com LGPD.

## 🔐 Authentication & Authorization

### User Authentication
- [ ] **Password security implementada**
  ```python
  # ✅ Secure password hashing
  from passlib.context import CryptContext
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  def hash_password(password: str) -> str:
      return pwd_context.hash(password)
  
  def verify_password(plain_password: str, hashed_password: str) -> bool:
      return pwd_context.verify(plain_password, hashed_password)
  ```

- [ ] **JWT token security**
  - Tokens têm expiração apropriada (15 min access, 7 days refresh)
  - Refresh token rotation implementada
  - Token revocation capability
  - Secure token storage no client

- [ ] **Session management seguro**
  ```python
  # ✅ Secure session configuration
  SESSION_CONFIG = {
      'httponly': True,
      'secure': True,  # HTTPS only
      'samesite': 'strict',
      'max_age': 900,  # 15 minutes
      'domain': None,  # No cross-domain
  }
  ```

### Authorization Controls
- [ ] **Role-based access control**
  - User roles claramente definidos (student, admin, analyst)
  - Permissions granulares para features
  - Resource-level access control
  - Privilege escalation prevention

- [ ] **API endpoint protection**
  ```python
  # ✅ Endpoint protection example
  @router.get("/admin/users", dependencies=[Depends(require_admin_role)])
  async def get_all_users(
      current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
  ):
      # Admin-only functionality
      pass
  
  @router.get("/user/profile")
  async def get_user_profile(
      current_user: User = Depends(get_current_user)
  ):
      # User can only access their own profile
      return current_user.profile
  ```

- [ ] **Data access validation**
  - Users can only access their own data
  - Cross-user data leakage prevented
  - Bulk operations restricted appropriately
  - Admin access logged and monitored

## 🛡️ Input Validation & Sanitization

### Input Validation
- [ ] **Comprehensive validation implemented**
  ```python
  # ✅ Robust input validation
  from pydantic import BaseModel, validator, Field
  from typing import Optional, List
  
  class QuizSubmission(BaseModel):
      quiz_id: int = Field(..., gt=0, description="Valid quiz ID")
      answers: List[str] = Field(..., max_items=100, description="User answers")
      time_spent: int = Field(..., ge=0, le=7200, description="Time in seconds")
      
      @validator('answers')
      def validate_answers(cls, v):
          if not v:
              raise ValueError('At least one answer required')
          
          # Sanitize each answer
          sanitized = []
          for answer in v:
              if len(answer) > 1000:
                  raise ValueError('Answer too long')
              sanitized.append(html.escape(answer.strip()))
          
          return sanitized
  ```

- [ ] **SQL injection prevention**
  - Parameterized queries used exclusively
  - ORM used correctly
  - Dynamic SQL avoided
  - Database permissions minimal

- [ ] **XSS protection**
  ```python
  # ✅ XSS prevention
  import html
  from markupsafe import Markup, escape
  
  def safe_render_user_content(content: str) -> str:
      """Safely render user-generated content."""
      # Escape HTML entities
      escaped = html.escape(content)
      
      # Allow safe markdown if needed
      if is_markdown_allowed():
          return markdown_to_safe_html(escaped)
      
      return escaped
  ```

### File Upload Security
- [ ] **File upload restrictions**
  ```python
  # ✅ Secure file upload
  ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
  MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
  
  def validate_file_upload(file: UploadFile) -> bool:
      # Check file extension
      file_ext = pathlib.Path(file.filename).suffix.lower()
      if file_ext not in ALLOWED_EXTENSIONS:
          raise ValueError(f"File type {file_ext} not allowed")
      
      # Check file size
      if file.size > MAX_FILE_SIZE:
          raise ValueError("File too large")
      
      # Check file content (not just extension)
      file_type = magic.from_buffer(file.file.read(), mime=True)
      if not is_safe_file_type(file_type):
          raise ValueError("File content validation failed")
      
      return True
  ```

## 🔒 Data Protection & Privacy

### LGPD Compliance
- [ ] **Data minimization implementada**
  - Apenas dados necessários coletados
  - Retenção por tempo limitado
  - Automatic data purging
  - Purpose limitation respected

- [ ] **Consent management**
  ```python
  # ✅ Granular consent management
  class UserConsent(Base):
      __tablename__ = "user_consents"
      
      user_id = Column(Integer, ForeignKey("users.id"))
      consent_type = Column(String, nullable=False)  # analytics, marketing, etc.
      granted = Column(Boolean, nullable=False)
      granted_at = Column(DateTime)
      withdrawn_at = Column(DateTime, nullable=True)
      
      # Purpose specification
      purpose = Column(String, nullable=False)
      legal_basis = Column(String, nullable=False)  # LGPD Article 7
      
      # Consent evidence
      consent_evidence = Column(JSON)  # How consent was obtained
  ```

- [ ] **Data subject rights implemented**
  - Right to access (data export)
  - Right to rectification (data correction)
  - Right to erasure (data deletion)
  - Right to portability
  - Right to object

### Educational Data Protection
- [ ] **Student data protection especial**
  ```python
  # ✅ Educational data protection
  class EducationalDataProtection:
      
      @staticmethod
      def anonymize_learning_data(data: dict) -> dict:
          """Anonymize learning data while preserving educational value."""
          anonymized = data.copy()
          
          # Remove direct identifiers
          anonymized.pop('user_id', None)
          anonymized.pop('email', None)
          anonymized.pop('name', None)
          
          # Hash indirect identifiers
          if 'session_id' in anonymized:
              anonymized['session_id'] = hash_identifier(anonymized['session_id'])
          
          # Add differential privacy to scores
          if 'scores' in anonymized:
              anonymized['scores'] = add_noise_to_scores(anonymized['scores'])
          
          return anonymized
  ```

- [ ] **Parental consent para menores**
  - Age verification implemented
  - Parental consent flow
  - Enhanced protection for minors
  - Educational institution consent

### Sensitive Data Handling
- [ ] **Data encryption**
  ```python
  # ✅ Data encryption at rest
  from cryptography.fernet import Fernet
  
  class DataEncryption:
      def __init__(self, key: bytes):
          self.cipher = Fernet(key)
      
      def encrypt_sensitive_data(self, data: str) -> str:
          """Encrypt sensitive personal data."""
          return self.cipher.encrypt(data.encode()).decode()
      
      def decrypt_sensitive_data(self, encrypted_data: str) -> str:
          """Decrypt sensitive personal data."""
          return self.cipher.decrypt(encrypted_data.encode()).decode()
  ```

- [ ] **Data transmission security**
  - HTTPS enforced everywhere
  - API keys transmitted securely
  - No sensitive data in URLs
  - Secure WebSocket connections

## 🔍 Security Monitoring & Logging

### Security Logging
- [ ] **Comprehensive audit trail**
  ```python
  # ✅ Security audit logging
  class SecurityAuditLogger:
      
      @staticmethod
      def log_authentication_event(user_id: int, event_type: str, success: bool, 
                                 ip_address: str, user_agent: str):
          """Log authentication events for security monitoring."""
          audit_log.info("Authentication event", extra={
              'event_type': 'authentication',
              'user_id': user_id,
              'auth_event': event_type,  # login, logout, failed_login
              'success': success,
              'ip_address': hash_ip_for_privacy(ip_address),
              'user_agent_hash': hash_user_agent(user_agent),
              'timestamp': datetime.utcnow(),
              'severity': 'high' if not success else 'info'
          })
      
      @staticmethod
      def log_data_access(user_id: int, resource_type: str, resource_id: str,
                         action: str, success: bool):
          """Log data access for LGPD compliance."""
          audit_log.info("Data access event", extra={
              'event_type': 'data_access',
              'user_id': user_id,
              'resource_type': resource_type,
              'resource_id': resource_id,
              'action': action,  # read, write, delete
              'success': success,
              'timestamp': datetime.utcnow()
          })
  ```

- [ ] **Privacy-preserving logs**
  - No PII in logs
  - IP addresses hashed
  - User agents hashed
  - Log retention policies

### Intrusion Detection
- [ ] **Automated threat detection**
  ```python
  # ✅ Rate limiting and abuse detection
  from slowapi import Limiter, _rate_limit_exceeded_handler
  from slowapi.util import get_remote_address
  
  limiter = Limiter(key_func=get_remote_address)
  
  @app.route("/api/login")
  @limiter.limit("5/minute")  # Max 5 login attempts per minute
  async def login_endpoint(request: Request):
      # Enhanced rate limiting for authentication
      pass
  
  # Suspicious activity detection
  class SuspiciousActivityDetector:
      
      def detect_unusual_patterns(self, user_id: int, activity: str):
          """Detect suspicious user activity patterns."""
          recent_activities = get_recent_activities(user_id, hours=1)
          
          # Check for unusual volume
          if len(recent_activities) > NORMAL_ACTIVITY_THRESHOLD:
              self.alert_security_team(f"Unusual activity volume for user {user_id}")
          
          # Check for unusual access patterns
          if self.is_unusual_access_pattern(recent_activities):
              self.alert_security_team(f"Unusual access pattern for user {user_id}")
  ```

## 🌐 Network & Infrastructure Security

### HTTPS & TLS
- [ ] **Strong TLS configuration**
  - TLS 1.2+ required
  - Strong cipher suites only
  - HSTS headers implemented
  - Certificate validation strict

- [ ] **Security headers implemented**
  ```python
  # ✅ Security headers
  SECURITY_HEADERS = {
      'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Content-Security-Policy': (
          "default-src 'self'; "
          "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
          "style-src 'self' 'unsafe-inline'; "
          "img-src 'self' data: https:; "
          "font-src 'self' https://fonts.gstatic.com;"
      ),
      'Referrer-Policy': 'strict-origin-when-cross-origin'
  }
  ```

### API Security
- [ ] **API security best practices**
  - Rate limiting implemented
  - API versioning secure
  - Input validation comprehensive
  - Output encoding consistent

- [ ] **CORS configuration secure**
  ```python
  # ✅ Secure CORS configuration
  CORS_CONFIG = {
      'allow_origins': ['https://agente-concurseiro.vercel.app'],
      'allow_credentials': True,
      'allow_methods': ['GET', 'POST', 'PUT', 'DELETE'],
      'allow_headers': ['Authorization', 'Content-Type'],
      'max_age': 600  # 10 minutes
  }
  ```

## 🔧 Third-Party Security

### AI Service Security
- [ ] **OpenAI API security**
  ```python
  # ✅ Secure AI API integration
  class SecureAIClient:
      def __init__(self, api_key: str):
          self.client = openai.AsyncClient(api_key=api_key)
          self.rate_limiter = AIRateLimiter()
      
      async def safe_ai_request(self, prompt: str, user_id: int) -> str:
          """Make secure AI request with data protection."""
          
          # Validate and sanitize prompt
          sanitized_prompt = self.sanitize_prompt(prompt)
          
          # Check for sensitive data
          if self.contains_sensitive_data(sanitized_prompt):
              raise SecurityError("Prompt contains sensitive data")
          
          # Rate limiting
          await self.rate_limiter.check_limits(user_id)
          
          # Make request with timeout
          try:
              response = await asyncio.wait_for(
                  self.client.chat.completions.create(
                      model="gpt-4",
                      messages=[{"role": "user", "content": sanitized_prompt}]
                  ),
                  timeout=30.0
              )
              
              # Log request (no content for privacy)
              security_logger.log_ai_request(user_id, "success", len(sanitized_prompt))
              
              return response.choices[0].message.content
              
          except Exception as e:
              security_logger.log_ai_request(user_id, "error", len(sanitized_prompt))
              raise
  ```

### External Service Integration
- [ ] **Webhook security**
  - Signature verification
  - IP allowlisting
  - Rate limiting
  - Request validation

- [ ] **API key management**
  - Keys stored securely (environment variables)
  - Key rotation implemented
  - Access logging
  - Minimal permissions

## 📱 Frontend Security

### Client-Side Security
- [ ] **Frontend data protection**
  ```javascript
  // ✅ Secure data handling no frontend
  class SecureDataHandler {
      
      static sanitizeUserInput(input) {
          // Remove script tags and other dangerous content
          return DOMPurify.sanitize(input, {
              ALLOWED_TAGS: ['b', 'i', 'em', 'strong'],
              ALLOWED_ATTR: []
          });
      }
      
      static secureLocalStorage(key, value) {
          // Encrypt sensitive data before storing
          if (this.isSensitiveData(key)) {
              value = this.encryptData(value);
          }
          localStorage.setItem(key, value);
      }
      
      static clearSensitiveData() {
          // Clear all sensitive data on logout
          const sensitiveKeys = ['auth_token', 'user_preferences'];
          sensitiveKeys.forEach(key => localStorage.removeItem(key));
      }
  }
  ```

### Streamlit Security
- [ ] **Streamlit security configuration**
  ```python
  # ✅ Secure Streamlit configuration
  def configure_streamlit_security():
      """Configure Streamlit with security best practices."""
      
      # Disable development features in production
      st.set_page_config(
          page_title="Agente Concurseiro",
          layout="wide",
          initial_sidebar_state="collapsed"
      )
      
      # Input sanitization for all user inputs
      def safe_text_input(label, key=None, **kwargs):
          value = st.text_input(label, key=key, **kwargs)
          return html.escape(value) if value else value
      
      # File upload with security checks
      def safe_file_uploader(label, **kwargs):
          file = st.file_uploader(label, **kwargs)
          if file:
              validate_uploaded_file(file)
          return file
  ```

## 🚨 Incident Response

### Security Incident Handling
- [ ] **Incident response plan**
  - Clear escalation procedures
  - Communication protocols
  - Evidence preservation
  - Recovery procedures

- [ ] **Automated incident detection**
  ```python
  # ✅ Security incident detection
  class SecurityIncidentDetector:
      
      def __init__(self):
          self.alert_thresholds = {
              'failed_logins': 10,  # per user per hour
              'data_access_volume': 1000,  # per user per hour
              'api_rate_exceeded': 5  # times per user per day
          }
      
      async def check_security_incidents(self):
          """Continuously monitor for security incidents."""
          
          # Check for brute force attacks
          suspicious_users = await self.detect_brute_force()
          for user_id in suspicious_users:
              await self.handle_brute_force_incident(user_id)
          
          # Check for data exfiltration
          high_volume_users = await self.detect_data_exfiltration()
          for user_id in high_volume_users:
              await self.handle_data_exfiltration_incident(user_id)
      
      async def handle_security_incident(self, incident_type: str, user_id: int):
          """Handle detected security incident."""
          
          # Log incident
          security_logger.log_incident(incident_type, user_id)
          
          # Immediate response
          if incident_type == "brute_force":
              await self.temporarily_lock_account(user_id)
          elif incident_type == "data_exfiltration":
              await self.rate_limit_user(user_id)
          
          # Notify security team
          await self.notify_security_team(incident_type, user_id)
  ```

## ✅ Security Testing

### Penetration Testing
- [ ] **Regular security assessments**
  - Automated vulnerability scanning
  - Manual penetration testing
  - Code security reviews
  - Infrastructure security audits

### Security Test Cases
- [ ] **Authentication testing**
  ```python
  # ✅ Security test examples
  class TestSecurity:
      
      def test_password_brute_force_protection(self):
          """Test that brute force attacks are prevented."""
          # Attempt multiple failed logins
          for i in range(15):
              response = self.client.post("/login", {
                  "email": "test@example.com",
                  "password": "wrong_password"
              })
          
          # Account should be locked
          response = self.client.post("/login", {
              "email": "test@example.com", 
              "password": "correct_password"
          })
          assert response.status_code == 423  # Locked
      
      def test_sql_injection_prevention(self):
          """Test that SQL injection attacks are prevented."""
          malicious_input = "'; DROP TABLE users; --"
          
          response = self.client.get(f"/search?q={malicious_input}")
          
          # Should not cause server error
          assert response.status_code != 500
          # Database should still exist
          assert User.query.count() > 0
  ```

## 📋 Security Checklist Final

### Pre-Deployment Security Review
- [ ] **All security controls implemented ✓**
- [ ] **LGPD compliance verified ✓**
- [ ] **Penetration testing completed ✓**
- [ ] **Security documentation updated ✓**
- [ ] **Incident response plan ready ✓**
- [ ] **Monitoring alerts configured ✓**
- [ ] **Security training completed ✓**

### Post-Deployment Security Monitoring
- [ ] **Security metrics tracking ✓**
- [ ] **Vulnerability scanning automated ✓**
- [ ] **Log analysis active ✓**
- [ ] **Incident response tested ✓**

---

**Critical Security Principles:**
1. **Defense in Depth**: Multiple layers of security
2. **Least Privilege**: Minimal necessary permissions
3. **Privacy by Design**: Privacy built in from the start
4. **Zero Trust**: Verify everything, trust nothing
5. **Continuous Monitoring**: Always watching for threats

**Remember**: Security is not optional. Any security vulnerability or privacy violation must be addressed immediately before deployment.

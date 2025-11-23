# Filter

Servlet Filter를 사용하여 HTTP 요청/응답을 필터링하는 방법을 알아봅니다.

## Filter란?

**Filter:** 서블릿 실행 전후로 요청과 응답을 필터링

### Filter vs Interceptor

| 특성 | Filter | Interceptor |
|------|--------|-------------|
| 영역 | Servlet | Spring MVC |
| 실행 시점 | DispatcherServlet 전후 | Controller 전후 |
| 설정 | web.xml 또는 @WebFilter | WebMvcConfigurer |
| 사용 | 인코딩, 보안, 압축 등 | 인증, 로깅, AOP 등 |
| Spring Bean 주입 | ❌ (설정 필요) | ✅ |

### 실행 순서

```
Client → Filter1 → Filter2 → DispatcherServlet → Interceptor → Controller
                                               ↓
Client ← Filter1 ← Filter2 ← DispatcherServlet ← Interceptor ← Controller
```

## Filter 구현

### 기본 Filter

```java
@Slf4j
@Component
public class LoggingFilter implements Filter {
    
    @Override
    public void init(FilterConfig filterConfig) {
        log.info("LoggingFilter initialized");
    }
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        long startTime = System.currentTimeMillis();
        
        log.info("[Filter] Request: {} {}", 
            httpRequest.getMethod(), 
            httpRequest.getRequestURI());
        
        try {
            chain.doFilter(request, response);  // 다음 필터로 전달
        } finally {
            long duration = System.currentTimeMillis() - startTime;
            log.info("[Filter] Response: {} - {}ms", 
                httpResponse.getStatus(), 
                duration);
        }
    }
    
    @Override
    public void destroy() {
        log.info("LoggingFilter destroyed");
    }
}
```

### 요청/응답 래핑 Filter

```java
@Slf4j
@Component
@Order(1)
public class RequestResponseLoggingFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        // 요청/응답 래핑
        ContentCachingRequestWrapper requestWrapper = 
            new ContentCachingRequestWrapper((HttpServletRequest) request);
        ContentCachingResponseWrapper responseWrapper = 
            new ContentCachingResponseWrapper((HttpServletResponse) response);
        
        try {
            chain.doFilter(requestWrapper, responseWrapper);
        } finally {
            // 요청 본문 로깅
            String requestBody = getRequestBody(requestWrapper);
            if (!requestBody.isEmpty()) {
                log.info("Request Body: {}", requestBody);
            }
            
            // 응답 본문 로깅
            String responseBody = getResponseBody(responseWrapper);
            if (!responseBody.isEmpty()) {
                log.info("Response Body: {}", responseBody);
            }
            
            // 응답 복사 (중요!)
            responseWrapper.copyBodyToResponse();
        }
    }
    
    private String getRequestBody(ContentCachingRequestWrapper request) {
        byte[] content = request.getContentAsByteArray();
        if (content.length > 0) {
            return new String(content, StandardCharsets.UTF_8);
        }
        return "";
    }
    
    private String getResponseBody(ContentCachingResponseWrapper response) {
        byte[] content = response.getContentAsByteArray();
        if (content.length > 0) {
            return new String(content, StandardCharsets.UTF_8);
        }
        return "";
    }
}
```

## 인코딩 Filter

### UTF-8 인코딩

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class EncodingFilter implements Filter {
    
    private static final String ENCODING = "UTF-8";
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        request.setCharacterEncoding(ENCODING);
        response.setCharacterEncoding(ENCODING);
        
        chain.doFilter(request, response);
    }
}
```

**또는 Spring Boot 기본 설정 사용:**

```yaml
server:
  servlet:
    encoding:
      charset: UTF-8
      enabled: true
      force: true
```

## CORS Filter

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorsFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        // CORS 헤더 설정
        httpResponse.setHeader("Access-Control-Allow-Origin", "*");
        httpResponse.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        httpResponse.setHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");
        httpResponse.setHeader("Access-Control-Max-Age", "3600");
        
        // OPTIONS 요청 처리
        if ("OPTIONS".equals(httpRequest.getMethod())) {
            httpResponse.setStatus(HttpServletResponse.SC_OK);
            return;
        }
        
        chain.doFilter(request, response);
    }
}
```

## XSS 방어 Filter

```java
@Slf4j
@Component
@Order(2)
public class XssFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        XssRequestWrapper wrappedRequest = new XssRequestWrapper((HttpServletRequest) request);
        chain.doFilter(wrappedRequest, response);
    }
}

public class XssRequestWrapper extends HttpServletRequestWrapper {
    
    public XssRequestWrapper(HttpServletRequest request) {
        super(request);
    }
    
    @Override
    public String getParameter(String name) {
        String value = super.getParameter(name);
        return sanitize(value);
    }
    
    @Override
    public String[] getParameterValues(String name) {
        String[] values = super.getParameterValues(name);
        if (values == null) {
            return null;
        }
        
        String[] sanitizedValues = new String[values.length];
        for (int i = 0; i < values.length; i++) {
            sanitizedValues[i] = sanitize(values[i]);
        }
        return sanitizedValues;
    }
    
    @Override
    public String getHeader(String name) {
        String value = super.getHeader(name);
        return sanitize(value);
    }
    
    private String sanitize(String value) {
        if (value == null) {
            return null;
        }
        
        // HTML 특수 문자 이스케이프
        return value.replaceAll("<", "&lt;")
                   .replaceAll(">", "&gt;")
                   .replaceAll("\"", "&quot;")
                   .replaceAll("'", "&#x27;")
                   .replaceAll("/", "&#x2F;");
    }
}
```

## IP 화이트리스트 Filter

```java
@Slf4j
@Component
public class IpWhitelistFilter implements Filter {
    
    private static final Set<String> WHITELIST = Set.of(
        "127.0.0.1",
        "192.168.1.100",
        "10.0.0.1"
    );
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        String clientIp = getClientIp(httpRequest);
        
        if (!WHITELIST.contains(clientIp)) {
            log.warn("Access denied from IP: {}", clientIp);
            httpResponse.setStatus(HttpServletResponse.SC_FORBIDDEN);
            httpResponse.getWriter().write("Access denied");
            return;
        }
        
        chain.doFilter(request, response);
    }
    
    private String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip == null || ip.isEmpty()) {
            ip = request.getHeader("X-Real-IP");
        }
        if (ip == null || ip.isEmpty()) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }
}
```

## JWT 인증 Filter

```java
@Slf4j
@RequiredArgsConstructor
@Component
public class JwtAuthenticationFilter implements Filter {
    
    private final JwtProvider jwtProvider;
    
    private static final List<String> EXCLUDE_URLS = List.of(
        "/api/v1/auth",
        "/api/v1/public",
        "/swagger-ui",
        "/api-docs"
    );
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        // 제외 URL 확인
        String requestURI = httpRequest.getRequestURI();
        if (isExcludeUrl(requestURI)) {
            chain.doFilter(request, response);
            return;
        }
        
        // JWT 토큰 검증
        try {
            String token = extractToken(httpRequest);
            if (token == null) {
                sendUnauthorizedResponse(httpResponse, "토큰이 없습니다");
                return;
            }
            
            if (!jwtProvider.validateToken(token)) {
                sendUnauthorizedResponse(httpResponse, "유효하지 않은 토큰입니다");
                return;
            }
            
            // 사용자 정보 설정
            String email = jwtProvider.extractUsername(token);
            httpRequest.setAttribute("userEmail", email);
            
            chain.doFilter(request, response);
            
        } catch (Exception e) {
            log.error("JWT authentication failed", e);
            sendUnauthorizedResponse(httpResponse, "인증 실패");
        }
    }
    
    private boolean isExcludeUrl(String requestURI) {
        return EXCLUDE_URLS.stream()
                .anyMatch(requestURI::startsWith);
    }
    
    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
    
    private void sendUnauthorizedResponse(HttpServletResponse response, String message) throws IOException {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("UNAUTHORIZED")
                .message(message)
                .timestamp(LocalDateTime.now())
                .build();
        
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.writeValue(response.getWriter(), errorResponse);
    }
}
```

## Filter 등록

### @Component 방식

```java
@Component
@Order(1)  // 실행 순서
public class MyFilter implements Filter {
    // ...
}
```

### FilterRegistrationBean 방식

```java
@Configuration
public class FilterConfig {
    
    @Bean
    public FilterRegistrationBean<LoggingFilter> loggingFilter() {
        FilterRegistrationBean<LoggingFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new LoggingFilter());
        registration.addUrlPatterns("/api/*");
        registration.setOrder(1);
        return registration;
    }
    
    @Bean
    public FilterRegistrationBean<AuthFilter> authFilter() {
        FilterRegistrationBean<AuthFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new AuthFilter());
        registration.addUrlPatterns("/api/private/*");
        registration.setOrder(2);
        return registration;
    }
}
```

## 실전 예제

### 요청 ID 추적 Filter

```java
@Slf4j
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestIdFilter implements Filter {
    
    private static final String REQUEST_ID_HEADER = "X-Request-ID";
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        // 요청 ID 생성 또는 추출
        String requestId = httpRequest.getHeader(REQUEST_ID_HEADER);
        if (requestId == null || requestId.isEmpty()) {
            requestId = UUID.randomUUID().toString();
        }
        
        // MDC에 저장 (로깅용)
        MDC.put("requestId", requestId);
        
        // 응답 헤더에 추가
        httpResponse.setHeader(REQUEST_ID_HEADER, requestId);
        
        try {
            log.info("Processing request: {} {} (ID: {})", 
                httpRequest.getMethod(), 
                httpRequest.getRequestURI(), 
                requestId);
            
            chain.doFilter(request, response);
            
        } finally {
            MDC.clear();
        }
    }
}
```

### 압축 Filter

```java
@Component
@Order(5)
public class CompressionFilter implements Filter {
    
    private static final int MIN_COMPRESS_SIZE = 1024;  // 1KB
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        String acceptEncoding = httpRequest.getHeader("Accept-Encoding");
        
        if (acceptEncoding != null && acceptEncoding.contains("gzip")) {
            GzipResponseWrapper gzipResponse = new GzipResponseWrapper(httpResponse);
            chain.doFilter(request, gzipResponse);
            gzipResponse.finish();
        } else {
            chain.doFilter(request, response);
        }
    }
}

public class GzipResponseWrapper extends HttpServletResponseWrapper {
    
    private GZIPOutputStream gzipOutputStream;
    private ServletOutputStream servletOutputStream;
    
    public GzipResponseWrapper(HttpServletResponse response) throws IOException {
        super(response);
        response.addHeader("Content-Encoding", "gzip");
    }
    
    @Override
    public ServletOutputStream getOutputStream() throws IOException {
        if (servletOutputStream == null) {
            gzipOutputStream = new GZIPOutputStream(getResponse().getOutputStream());
            servletOutputStream = new ServletOutputStream() {
                @Override
                public void write(int b) throws IOException {
                    gzipOutputStream.write(b);
                }
                
                @Override
                public boolean isReady() {
                    return true;
                }
                
                @Override
                public void setWriteListener(WriteListener listener) {
                }
            };
        }
        return servletOutputStream;
    }
    
    public void finish() throws IOException {
        if (gzipOutputStream != null) {
            gzipOutputStream.finish();
        }
    }
}
```

## 실전 팁

### 1. Filter 순서

```java
@Order(1)  // 숫자가 작을수록 먼저 실행
public class FirstFilter implements Filter { }

@Order(2)
public class SecondFilter implements Filter { }

// 또는
FilterRegistrationBean<MyFilter> registration = new FilterRegistrationBean<>();
registration.setOrder(1);
```

### 2. URL 패턴

```java
@Bean
public FilterRegistrationBean<MyFilter> myFilter() {
    FilterRegistrationBean<MyFilter> registration = new FilterRegistrationBean<>();
    registration.setFilter(new MyFilter());
    
    // URL 패턴 지정
    registration.addUrlPatterns("/api/*");
    registration.addUrlPatterns("/admin/*");
    
    return registration;
}
```

### 3. 조건부 Filter

```java
@Component
@ConditionalOnProperty(name = "app.security.enabled", havingValue = "true")
public class SecurityFilter implements Filter {
    // app.security.enabled=true일 때만 활성화
}
```

### 4. Filter Chain 중단

```java
@Override
public void doFilter(ServletRequest request, 
                    ServletResponse response, 
                    FilterChain chain) throws IOException, ServletException {
    
    if (shouldBlock(request)) {
        // Filter chain을 진행하지 않음
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        httpResponse.setStatus(HttpServletResponse.SC_FORBIDDEN);
        httpResponse.getWriter().write("Blocked");
        return;  // chain.doFilter() 호출 안 함
    }
    
    chain.doFilter(request, response);
}
```

## 다음 단계

Filter를 배웠습니다. 이제 AOP를 알아봅시다.

👉 [다음: AOP](24-aop.md)

## 참고 자료

- [Servlet Filter](https://docs.oracle.com/javaee/7/api/javax/servlet/Filter.html)
- [Spring Boot Filter](https://docs.spring.io/spring-boot/docs/current/reference/html/web.html#web.servlet.embedded-container.context-initializer)

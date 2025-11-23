# Interceptor

HandlerInterceptor를 사용하여 HTTP 요청/응답을 가로채는 방법을 알아봅니다.

## Interceptor란?

**Interceptor:** Controller 실행 전후로 요청과 응답을 가로채서 처리

### 실행 순서

```
Filter → Interceptor → AOP → Controller
                     ↓
Filter ← Interceptor ← AOP ← Controller
```

### 주요 메서드

```java
public interface HandlerInterceptor {
    
    // Controller 실행 전
    boolean preHandle(HttpServletRequest request, 
                     HttpServletResponse response, 
                     Object handler);
    
    // Controller 실행 후, View 렌더링 전
    void postHandle(HttpServletRequest request, 
                   HttpServletResponse response, 
                   Object handler, 
                   ModelAndView modelAndView);
    
    // View 렌더링 후 (요청 완료)
    void afterCompletion(HttpServletRequest request, 
                        HttpServletResponse response, 
                        Object handler, 
                        Exception ex);
}
```

## Interceptor 구현

### 로깅 Interceptor

```java
@Slf4j
@Component
public class LoggingInterceptor implements HandlerInterceptor {
    
    private static final String START_TIME = "startTime";
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        long startTime = System.currentTimeMillis();
        request.setAttribute(START_TIME, startTime);
        
        log.info("[REQUEST] {} {} from {}",
            request.getMethod(),
            request.getRequestURI(),
            request.getRemoteAddr());
        
        return true;  // true: 다음 단계 진행, false: 중단
    }
    
    @Override
    public void postHandle(HttpServletRequest request, 
                          HttpServletResponse response, 
                          Object handler, 
                          ModelAndView modelAndView) {
        log.info("[RESPONSE] Status: {}", response.getStatus());
    }
    
    @Override
    public void afterCompletion(HttpServletRequest request, 
                               HttpServletResponse response, 
                               Object handler, 
                               Exception ex) {
        long startTime = (Long) request.getAttribute(START_TIME);
        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        
        log.info("[COMPLETED] {} {} - {}ms",
            request.getMethod(),
            request.getRequestURI(),
            duration);
        
        if (ex != null) {
            log.error("[ERROR] Exception occurred", ex);
        }
    }
}
```

### 인증 Interceptor

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {
    
    private final JwtProvider jwtProvider;
    private final UserService userService;
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) throws IOException {
        
        // OPTIONS 요청은 통과
        if ("OPTIONS".equals(request.getMethod())) {
            return true;
        }
        
        // Handler 확인
        if (!(handler instanceof HandlerMethod)) {
            return true;
        }
        
        // @NoAuth 어노테이션이 있으면 통과
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        if (handlerMethod.hasMethodAnnotation(NoAuth.class)) {
            return true;
        }
        
        // JWT 토큰 검증
        String token = extractToken(request);
        if (token == null) {
            sendUnauthorizedResponse(response, "토큰이 없습니다");
            return false;
        }
        
        try {
            String email = jwtProvider.extractUsername(token);
            User user = userService.getUserByEmail(email);
            
            // 요청에 사용자 정보 설정
            request.setAttribute("userId", user.getId());
            request.setAttribute("userEmail", user.getEmail());
            
            return true;
        } catch (Exception e) {
            log.error("Token validation failed", e);
            sendUnauthorizedResponse(response, "유효하지 않은 토큰입니다");
            return false;
        }
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

### 권한 검사 Interceptor

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class RoleInterceptor implements HandlerInterceptor {
    
    private final UserService userService;
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) throws IOException {
        
        if (!(handler instanceof HandlerMethod)) {
            return true;
        }
        
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        
        // @RequireRole 어노테이션 확인
        RequireRole requireRole = handlerMethod.getMethodAnnotation(RequireRole.class);
        if (requireRole == null) {
            return true;
        }
        
        // 사용자 정보 가져오기
        Long userId = (Long) request.getAttribute("userId");
        if (userId == null) {
            sendForbiddenResponse(response, "인증이 필요합니다");
            return false;
        }
        
        User user = userService.getUser(userId);
        Role userRole = user.getRole();
        
        // 권한 확인
        Role[] requiredRoles = requireRole.value();
        boolean hasRole = Arrays.stream(requiredRoles)
                .anyMatch(role -> role == userRole);
        
        if (!hasRole) {
            log.warn("Access denied for user {} to {}", user.getEmail(), request.getRequestURI());
            sendForbiddenResponse(response, "권한이 없습니다");
            return false;
        }
        
        return true;
    }
    
    private void sendForbiddenResponse(HttpServletResponse response, String message) throws IOException {
        response.setStatus(HttpServletResponse.SC_FORBIDDEN);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("FORBIDDEN")
                .message(message)
                .timestamp(LocalDateTime.now())
                .build();
        
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.writeValue(response.getWriter(), errorResponse);
    }
}
```

## Interceptor 등록

### WebMvcConfigurer

```java
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {
    
    private final LoggingInterceptor loggingInterceptor;
    private final AuthInterceptor authInterceptor;
    private final RoleInterceptor roleInterceptor;
    
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 로깅 인터셉터 (모든 요청)
        registry.addInterceptor(loggingInterceptor)
                .addPathPatterns("/**")
                .order(1);
        
        // 인증 인터셉터
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns(
                    "/api/v1/auth/**",
                    "/api/v1/public/**",
                    "/swagger-ui/**",
                    "/api-docs/**"
                )
                .order(2);
        
        // 권한 인터셉터
        registry.addInterceptor(roleInterceptor)
                .addPathPatterns("/api/**")
                .order(3);
    }
}
```

## 커스텀 어노테이션

### @NoAuth

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface NoAuth {
}
```

### @RequireRole

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireRole {
    Role[] value();
}
```

### 사용 예시

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    // 인증 불필요
    @NoAuth
    @GetMapping("/public")
    public ResponseEntity<String> publicEndpoint() {
        return ResponseEntity.ok("Public endpoint");
    }
    
    // 인증 필요
    @GetMapping("/me")
    public ResponseEntity<UserResponse> getMyInfo(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ResponseEntity.ok(userService.getUser(userId));
    }
    
    // ADMIN 권한 필요
    @RequireRole(Role.ADMIN)
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }
    
    // ADMIN 또는 MANAGER 권한 필요
    @RequireRole({Role.ADMIN, Role.MANAGER})
    @GetMapping("/reports")
    public ResponseEntity<List<ReportResponse>> getReports() {
        return ResponseEntity.ok(reportService.getReports());
    }
}
```

## 실전 예제

### API 호출 제한 (Rate Limiting)

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class RateLimitInterceptor implements HandlerInterceptor {
    
    private final RedisTemplate<String, String> redisTemplate;
    private static final int MAX_REQUESTS = 100;
    private static final Duration WINDOW = Duration.ofMinutes(1);
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) throws IOException {
        
        String clientIp = getClientIp(request);
        String key = "rate_limit:" + clientIp;
        
        // 현재 요청 수 조회
        String countStr = redisTemplate.opsForValue().get(key);
        int count = countStr != null ? Integer.parseInt(countStr) : 0;
        
        if (count >= MAX_REQUESTS) {
            log.warn("Rate limit exceeded for IP: {}", clientIp);
            sendTooManyRequestsResponse(response);
            return false;
        }
        
        // 요청 수 증가
        if (count == 0) {
            redisTemplate.opsForValue().set(key, "1", WINDOW);
        } else {
            redisTemplate.opsForValue().increment(key);
        }
        
        return true;
    }
    
    private String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip == null || ip.isEmpty()) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }
    
    private void sendTooManyRequestsResponse(HttpServletResponse response) throws IOException {
        response.setStatus(HttpServletResponse.SC_TOO_MANY_REQUESTS);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("TOO_MANY_REQUESTS")
                .message("요청 한도를 초과했습니다")
                .timestamp(LocalDateTime.now())
                .build();
        
        new ObjectMapper()
                .registerModule(new JavaTimeModule())
                .writeValue(response.getWriter(), errorResponse);
    }
}
```

### API 버전 체크

```java
@Slf4j
@Component
public class ApiVersionInterceptor implements HandlerInterceptor {
    
    private static final String MIN_VERSION = "1.0.0";
    private static final String MAX_VERSION = "2.0.0";
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) throws IOException {
        
        String version = request.getHeader("API-Version");
        
        if (version == null) {
            sendBadRequestResponse(response, "API 버전 헤더가 필요합니다");
            return false;
        }
        
        if (!isValidVersion(version)) {
            sendBadRequestResponse(response, 
                String.format("지원하지 않는 API 버전입니다. (지원 범위: %s - %s)", 
                    MIN_VERSION, MAX_VERSION));
            return false;
        }
        
        request.setAttribute("apiVersion", version);
        return true;
    }
    
    private boolean isValidVersion(String version) {
        try {
            // 간단한 버전 비교 (실제로는 Semantic Versioning 라이브러리 사용 권장)
            return version.compareTo(MIN_VERSION) >= 0 
                && version.compareTo(MAX_VERSION) <= 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    private void sendBadRequestResponse(HttpServletResponse response, String message) throws IOException {
        response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("BAD_REQUEST")
                .message(message)
                .timestamp(LocalDateTime.now())
                .build();
        
        new ObjectMapper()
                .registerModule(new JavaTimeModule())
                .writeValue(response.getWriter(), errorResponse);
    }
}
```

### 요청/응답 로깅

```java
@Slf4j
@Component
public class DetailedLoggingInterceptor implements HandlerInterceptor {
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        
        log.info("========== REQUEST ==========");
        log.info("URL: {} {}", request.getMethod(), request.getRequestURI());
        log.info("Client IP: {}", getClientIp(request));
        log.info("User-Agent: {}", request.getHeader("User-Agent"));
        
        // 헤더 로깅
        Enumeration<String> headerNames = request.getHeaderNames();
        while (headerNames.hasMoreElements()) {
            String headerName = headerNames.nextElement();
            log.info("Header: {} = {}", headerName, request.getHeader(headerName));
        }
        
        // 파라미터 로깅
        Map<String, String[]> params = request.getParameterMap();
        for (Map.Entry<String, String[]> entry : params.entrySet()) {
            log.info("Parameter: {} = {}", entry.getKey(), Arrays.toString(entry.getValue()));
        }
        
        return true;
    }
    
    @Override
    public void afterCompletion(HttpServletRequest request, 
                               HttpServletResponse response, 
                               Object handler, 
                               Exception ex) {
        
        log.info("========== RESPONSE ==========");
        log.info("Status: {}", response.getStatus());
        log.info("Content-Type: {}", response.getContentType());
        
        if (ex != null) {
            log.error("Exception: ", ex);
        }
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

## 실전 팁

### 1. 실행 순서 제어

```java
@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(loggingInterceptor).order(1);     // 먼저 실행
    registry.addInterceptor(authInterceptor).order(2);        // 그 다음
    registry.addInterceptor(roleInterceptor).order(3);        // 마지막
}
```

### 2. 패턴 매칭

```java
registry.addInterceptor(authInterceptor)
        .addPathPatterns("/api/**")           // 포함
        .excludePathPatterns(                 // 제외
            "/api/public/**",
            "/api/v1/auth/**"
        );
```

### 3. ThreadLocal 사용

```java
public class UserContextHolder {
    
    private static final ThreadLocal<User> userContext = new ThreadLocal<>();
    
    public static void setUser(User user) {
        userContext.set(user);
    }
    
    public static User getUser() {
        return userContext.get();
    }
    
    public static void clear() {
        userContext.remove();
    }
}

// Interceptor에서 설정
@Override
public boolean preHandle(HttpServletRequest request, 
                        HttpServletResponse response, 
                        Object handler) {
    User user = getCurrentUser(request);
    UserContextHolder.setUser(user);
    return true;
}

@Override
public void afterCompletion(HttpServletRequest request, 
                           HttpServletResponse response, 
                           Object handler, 
                           Exception ex) {
    UserContextHolder.clear();  // 반드시 정리
}
```

### 4. 비동기 요청 처리

```java
@Component
public class AsyncInterceptor implements AsyncHandlerInterceptor {
    
    @Override
    public void afterConcurrentHandlingStarted(HttpServletRequest request, 
                                              HttpServletResponse response, 
                                              Object handler) {
        // 비동기 처리 시작 시 호출
        log.info("Async handling started");
    }
}
```

## 다음 단계

Interceptor를 배웠습니다. 이제 Filter를 알아봅시다.

👉 [다음: Filter](23-filter.md)

## 참고 자료

- [Spring MVC Interceptor](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-config-interceptors)
- [HandlerInterceptor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/HandlerInterceptor.html)

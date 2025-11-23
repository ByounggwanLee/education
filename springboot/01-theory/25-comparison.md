# Filter vs Interceptor vs AOP

Filter, Interceptor, AOP의 차이점과 사용 시나리오를 비교합니다.

## 실행 순서

```
Client
  ↓
[Filter]                 ← Servlet 영역
  ↓
DispatcherServlet
  ↓
[Interceptor]           ← Spring MVC 영역
  ↓
[AOP]                   ← Spring AOP 영역
  ↓
Controller
  ↓
Service
  ↓
Repository
```

## 비교표

| 특성 | Filter | Interceptor | AOP |
|------|--------|-------------|-----|
| **영역** | Servlet | Spring MVC | Spring Bean |
| **실행 시점** | DispatcherServlet 전후 | Controller 전후 | 메서드 실행 전후 |
| **설정 방법** | web.xml 또는 @WebFilter | WebMvcConfigurer | @Aspect |
| **Spring Bean 주입** | ❌ (설정 필요) | ✅ | ✅ |
| **URL 패턴** | ✅ | ✅ | ❌ |
| **메서드 지정** | ❌ | ❌ | ✅ |
| **파라미터 접근** | ServletRequest | HttpServletRequest | JoinPoint |
| **예외 처리** | try-catch | try-catch | @AfterThrowing |
| **순서 제어** | @Order | addInterceptor().order() | @Order |

## 사용 시나리오

### Filter 사용

```java
✅ 인코딩 설정
✅ 보안 관련 처리 (XSS, CSRF)
✅ 압축/암호화
✅ 로깅 (요청/응답 전체)
✅ 인증 (Spring Security Filter)
✅ CORS 설정
✅ IP 차단
```

### Interceptor 사용

```java
✅ 인증/인가 (Controller 진입 전)
✅ 로깅 (Controller 레벨)
✅ API 버전 체크
✅ Rate Limiting
✅ 사용자 컨텍스트 설정
✅ 요청 ID 생성
```

### AOP 사용

```java
✅ 로깅 (메서드 레벨)
✅ 트랜잭션 처리
✅ 성능 측정
✅ 캐싱
✅ 재시도 로직
✅ 권한 검사 (메서드 레벨)
✅ 예외 변환
```

## 실전 예제

### 인증 처리 비교

#### Filter로 구현

```java
@Component
@Order(1)
public class AuthFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        String token = httpRequest.getHeader("Authorization");
        
        if (token == null || !validateToken(token)) {
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }
        
        chain.doFilter(request, response);
    }
    
    private boolean validateToken(String token) {
        // 토큰 검증
        return true;
    }
}
```

**장점:**
- ✅ 모든 요청에 대해 가장 먼저 실행
- ✅ DispatcherServlet 도달 전에 차단 가능

**단점:**
- ❌ Spring Context 접근 어려움
- ❌ URL 패턴 매칭만 가능

#### Interceptor로 구현

```java
@Component
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {
    
    private final JwtProvider jwtProvider;
    private final UserService userService;
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) throws IOException {
        
        // @NoAuth 어노테이션 확인
        if (handler instanceof HandlerMethod) {
            HandlerMethod handlerMethod = (HandlerMethod) handler;
            if (handlerMethod.hasMethodAnnotation(NoAuth.class)) {
                return true;
            }
        }
        
        String token = extractToken(request);
        if (token == null || !jwtProvider.validateToken(token)) {
            sendUnauthorizedResponse(response);
            return false;
        }
        
        // 사용자 정보 설정
        String email = jwtProvider.extractUsername(token);
        User user = userService.getUserByEmail(email);
        request.setAttribute("currentUser", user);
        
        return true;
    }
    
    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
    
    private void sendUnauthorizedResponse(HttpServletResponse response) throws IOException {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.getWriter().write("{\"error\":\"Unauthorized\"}");
    }
}
```

**장점:**
- ✅ Spring Bean 주입 가능
- ✅ Handler 정보 접근 가능 (어노테이션 확인)
- ✅ URL 패턴 매칭

**단점:**
- ❌ DispatcherServlet 이후에 실행

#### AOP로 구현

```java
@Aspect
@Component
@RequiredArgsConstructor
public class AuthAspect {
    
    private final UserContextHolder userContextHolder;
    
    @Before("@annotation(requireAuth)")
    public void checkAuth(JoinPoint joinPoint, RequireAuth requireAuth) {
        User user = userContextHolder.getCurrentUser();
        
        if (user == null) {
            throw new UnauthorizedException("인증이 필요합니다");
        }
        
        Role[] requiredRoles = requireAuth.value();
        if (requiredRoles.length > 0) {
            boolean hasRole = Arrays.stream(requiredRoles)
                    .anyMatch(role -> role == user.getRole());
            
            if (!hasRole) {
                throw new ForbiddenException("권한이 없습니다");
            }
        }
    }
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireAuth {
    Role[] value() default {};
}

// 사용
@Service
public class UserService {
    
    @RequireAuth
    public UserResponse getUser(Long id) {
        // ...
    }
    
    @RequireAuth(Role.ADMIN)
    public void deleteUser(Long id) {
        // ...
    }
}
```

**장점:**
- ✅ 메서드 단위 제어
- ✅ 비즈니스 로직 분리
- ✅ 어노테이션 기반 간결한 코드

**단점:**
- ❌ HTTP 요청/응답 직접 접근 어려움
- ❌ Controller 도달 후 실행

### 로깅 비교

#### Filter로 로깅

```java
@Component
@Slf4j
public class LoggingFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        
        log.info("[Filter] {} {} from {}",
            httpRequest.getMethod(),
            httpRequest.getRequestURI(),
            httpRequest.getRemoteAddr());
        
        chain.doFilter(request, response);
    }
}
```

**사용 사례:** 모든 HTTP 요청 로깅

#### Interceptor로 로깅

```java
@Component
@Slf4j
public class LoggingInterceptor implements HandlerInterceptor {
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        
        if (handler instanceof HandlerMethod) {
            HandlerMethod method = (HandlerMethod) handler;
            log.info("[Interceptor] Controller: {}.{}",
                method.getBeanType().getSimpleName(),
                method.getMethod().getName());
        }
        
        return true;
    }
}
```

**사용 사례:** Controller 진입 시점 로깅

#### AOP로 로깅

```java
@Aspect
@Component
@Slf4j
public class LoggingAspect {
    
    @Around("execution(* com.example.service..*.*(..))")
    public Object logMethodExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        String className = joinPoint.getSignature().getDeclaringTypeName();
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        
        log.info("[AOP] >>> {}.{} args: {}", className, methodName, Arrays.toString(args));
        
        Object result = joinPoint.proceed();
        
        log.info("[AOP] <<< {}.{} result: {}", className, methodName, result);
        
        return result;
    }
}
```

**사용 사례:** Service 메서드 실행 로깅

## 조합 사용 예제

### 완전한 요청 처리 흐름

```java
// 1. Filter: 모든 요청에 대한 인코딩 설정
@Component
@Order(1)
public class EncodingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");
        chain.doFilter(request, response);
    }
}

// 2. Filter: 요청 ID 생성
@Component
@Order(2)
public class RequestIdFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        String requestId = UUID.randomUUID().toString();
        MDC.put("requestId", requestId);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}

// 3. Interceptor: 인증 처리
@Component
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {
    private final JwtProvider jwtProvider;
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        String token = extractToken(request);
        if (!jwtProvider.validateToken(token)) {
            return false;
        }
        return true;
    }
}

// 4. Interceptor: 권한 검사
@Component
@RequiredArgsConstructor
public class RoleInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        // 권한 검사 로직
        return true;
    }
}

// 5. AOP: Service 메서드 로깅
@Aspect
@Component
@Slf4j
public class ServiceLoggingAspect {
    @Around("execution(* com.example.service..*.*(..))")
    public Object log(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("Service method: {}", joinPoint.getSignature());
        return joinPoint.proceed();
    }
}

// 6. AOP: 트랜잭션 로깅
@Aspect
@Component
@Slf4j
public class TransactionAspect {
    @Before("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void logTransaction(JoinPoint joinPoint) {
        log.info("Transaction started: {}", joinPoint.getSignature());
    }
}

// 7. Controller
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }
}

// 8. Service
@Service
@RequiredArgsConstructor
public class UserService {
    
    @Transactional(readOnly = true)
    public UserResponse getUser(Long id) {
        // 비즈니스 로직
        return UserResponse.from(userRepository.findById(id).orElseThrow());
    }
}
```

## 실전 가이드

### 언제 Filter를 사용할까?

```java
✅ 모든 요청에 공통 처리 필요
✅ Spring Context 없이 동작
✅ 인코딩, 압축, 암호화
✅ IP 차단, Rate Limiting
✅ CORS 설정
```

**예시:**
```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorsFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        httpResponse.setHeader("Access-Control-Allow-Origin", "*");
        httpResponse.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
        chain.doFilter(request, response);
    }
}
```

### 언제 Interceptor를 사용할까?

```java
✅ Controller 진입 전 처리
✅ Spring Bean 주입 필요
✅ Handler 정보 필요
✅ URL 패턴별 처리
✅ 인증/인가
```

**예시:**
```java
@Component
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {
    private final JwtProvider jwtProvider;
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                            HttpServletResponse response, 
                            Object handler) {
        // JWT 검증 후 사용자 정보 설정
        return true;
    }
}
```

### 언제 AOP를 사용할까?

```java
✅ 메서드 단위 처리
✅ 비즈니스 로직 분리
✅ 트랜잭션, 캐싱
✅ 성능 측정
✅ 예외 처리
```

**예시:**
```java
@Aspect
@Component
public class PerformanceAspect {
    @Around("@annotation(Monitored)")
    public Object measureTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;
        log.info("{} took {}ms", joinPoint.getSignature(), duration);
        return result;
    }
}
```

## 성능 고려사항

### Filter

```java
// ✅ 좋은 예: 필요한 URL만 필터링
FilterRegistrationBean<MyFilter> registration = new FilterRegistrationBean<>();
registration.addUrlPatterns("/api/*");

// ❌ 나쁜 예: 모든 요청 필터링
registration.addUrlPatterns("/*");
```

### Interceptor

```java
// ✅ 좋은 예: 필요한 경로만 적용
@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(authInterceptor)
            .addPathPatterns("/api/**")
            .excludePathPatterns("/api/public/**");
}

// ❌ 나쁜 예: 모든 경로에 적용
registry.addInterceptor(authInterceptor).addPathPatterns("/**");
```

### AOP

```java
// ✅ 좋은 예: 어노테이션 기반 선택적 적용
@Around("@annotation(Monitored)")
public Object monitor(ProceedingJoinPoint joinPoint) { }

// ❌ 나쁜 예: 모든 메서드에 적용
@Around("execution(* *.*(..))")
public Object monitor(ProceedingJoinPoint joinPoint) { }
```

## 다음 단계

Filter, Interceptor, AOP 비교를 배웠습니다. 이제 Actuator를 알아봅시다.

👉 [다음: Actuator](26-actuator.md)

## 참고 자료

- [Spring MVC Filters](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#filters)
- [Spring MVC Interceptors](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-config-interceptors)
- [Spring AOP](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop)

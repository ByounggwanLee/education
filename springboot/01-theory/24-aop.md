# AOP (Aspect-Oriented Programming)

관점 지향 프로그래밍을 통해 횡단 관심사를 분리하는 방법을 알아봅니다.

## AOP란?

**AOP:** 공통 기능을 비즈니스 로직에서 분리하여 모듈화

### 주요 개념

- **Aspect:** 공통 기능을 모듈화한 것
- **Join Point:** Aspect가 적용될 수 있는 지점
- **Pointcut:** Join Point를 선택하는 표현식
- **Advice:** 실제 실행되는 코드 (Before, After, Around 등)
- **Weaving:** Aspect를 대상 객체에 적용하는 과정

### 사용 사례

- ✅ 로깅
- ✅ 트랜잭션 처리
- ✅ 보안 검사
- ✅ 성능 측정
- ✅ 예외 처리

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

### Gradle

```gradle
implementation 'org.springframework.boot:spring-boot-starter-aop'
```

## AOP 활성화

```java
@SpringBootApplication
@EnableAspectJAutoProxy
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## Advice 종류

### @Before

```java
@Aspect
@Component
@Slf4j
public class LoggingAspect {
    
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        log.info("[Before] {}.{}",
            joinPoint.getSignature().getDeclaringTypeName(),
            joinPoint.getSignature().getName());
    }
}
```

### @After

```java
@After("execution(* com.example.service.*.*(..))")
public void logAfter(JoinPoint joinPoint) {
    log.info("[After] {}.{}",
        joinPoint.getSignature().getDeclaringTypeName(),
        joinPoint.getSignature().getName());
}
```

### @AfterReturning

```java
@AfterReturning(
    pointcut = "execution(* com.example.service.*.*(..))",
    returning = "result"
)
public void logAfterReturning(JoinPoint joinPoint, Object result) {
    log.info("[AfterReturning] {}.{} returned: {}",
        joinPoint.getSignature().getDeclaringTypeName(),
        joinPoint.getSignature().getName(),
        result);
}
```

### @AfterThrowing

```java
@AfterThrowing(
    pointcut = "execution(* com.example.service.*.*(..))",
    throwing = "exception"
)
public void logAfterThrowing(JoinPoint joinPoint, Exception exception) {
    log.error("[AfterThrowing] {}.{} threw: {}",
        joinPoint.getSignature().getDeclaringTypeName(),
        joinPoint.getSignature().getName(),
        exception.getMessage());
}
```

### @Around

```java
@Around("execution(* com.example.service.*.*(..))")
public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
    long startTime = System.currentTimeMillis();
    
    log.info("[Around-Before] {}.{}",
        joinPoint.getSignature().getDeclaringTypeName(),
        joinPoint.getSignature().getName());
    
    try {
        Object result = joinPoint.proceed();  // 메서드 실행
        
        long duration = System.currentTimeMillis() - startTime;
        log.info("[Around-After] {}.{} executed in {}ms",
            joinPoint.getSignature().getDeclaringTypeName(),
            joinPoint.getSignature().getName(),
            duration);
        
        return result;
    } catch (Exception e) {
        log.error("[Around-Error] {}.{} threw exception",
            joinPoint.getSignature().getDeclaringTypeName(),
            joinPoint.getSignature().getName(),
            e);
        throw e;
    }
}
```

## Pointcut 표현식

### execution

```java
// 모든 public 메서드
@Pointcut("execution(public * *(..))")

// UserService의 모든 메서드
@Pointcut("execution(* com.example.service.UserService.*(..))")

// service 패키지의 모든 메서드
@Pointcut("execution(* com.example.service.*.*(..))")

// service 패키지와 하위 패키지의 모든 메서드
@Pointcut("execution(* com.example.service..*.*(..))")

// 반환 타입이 User인 메서드
@Pointcut("execution(com.example.domain.User *(..))")

// 파라미터가 없는 메서드
@Pointcut("execution(* *())")

// 파라미터가 1개인 메서드
@Pointcut("execution(* *(*))")

// 파라미터가 Long 타입 1개인 메서드
@Pointcut("execution(* *(Long))")

// 파라미터가 여러 개인 메서드
@Pointcut("execution(* *(..))")
```

### within

```java
// UserService 클래스의 모든 메서드
@Pointcut("within(com.example.service.UserService)")

// service 패키지의 모든 클래스
@Pointcut("within(com.example.service.*)")

// service 패키지와 하위 패키지
@Pointcut("within(com.example.service..*)")
```

### @annotation

```java
// @Loggable 어노테이션이 붙은 메서드
@Pointcut("@annotation(com.example.annotation.Loggable)")

// @Transactional 어노테이션이 붙은 메서드
@Pointcut("@annotation(org.springframework.transaction.annotation.Transactional)")
```

### 조합

```java
// AND
@Pointcut("execution(* com.example.service.*.*(..)) && @annotation(com.example.annotation.Loggable)")

// OR
@Pointcut("execution(* com.example.service.*.*(..)) || execution(* com.example.controller.*.*(..))")

// NOT
@Pointcut("execution(* com.example.service.*.*(..)) && !@annotation(com.example.annotation.NoLogging)")
```

## 실전 예제

### 로깅 Aspect

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
        
        log.info(">>> {}.{} called with args: {}", className, methodName, Arrays.toString(args));
        
        long startTime = System.currentTimeMillis();
        
        try {
            Object result = joinPoint.proceed();
            long duration = System.currentTimeMillis() - startTime;
            
            log.info("<<< {}.{} returned: {} ({}ms)", 
                className, methodName, result, duration);
            
            return result;
        } catch (Exception e) {
            log.error("!!! {}.{} threw exception: {}", 
                className, methodName, e.getMessage());
            throw e;
        }
    }
}
```

### 성능 측정 Aspect

```java
@Aspect
@Component
@Slf4j
public class PerformanceAspect {
    
    @Around("@annotation(com.example.annotation.Timed)")
    public Object measureExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        
        try {
            return joinPoint.proceed();
        } finally {
            long duration = System.currentTimeMillis() - startTime;
            String methodName = joinPoint.getSignature().toShortString();
            
            log.info("[Performance] {} executed in {}ms", methodName, duration);
            
            // 느린 쿼리 경고
            if (duration > 1000) {
                log.warn("[Slow Method] {} took {}ms", methodName, duration);
            }
        }
    }
}

// 어노테이션
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Timed {
}

// 사용
@Service
public class UserService {
    
    @Timed
    public UserResponse getUser(Long id) {
        // ...
    }
}
```

### 캐시 Aspect

```java
@Aspect
@Component
@Slf4j
@RequiredArgsConstructor
public class CacheAspect {
    
    private final ConcurrentHashMap<String, Object> cache = new ConcurrentHashMap<>();
    
    @Around("@annotation(cacheable)")
    public Object cacheResult(ProceedingJoinPoint joinPoint, Cacheable cacheable) throws Throwable {
        String key = generateKey(joinPoint);
        
        // 캐시 확인
        if (cache.containsKey(key)) {
            log.info("[Cache Hit] {}", key);
            return cache.get(key);
        }
        
        // 캐시 미스 - 실행 후 저장
        log.info("[Cache Miss] {}", key);
        Object result = joinPoint.proceed();
        cache.put(key, result);
        
        return result;
    }
    
    private String generateKey(ProceedingJoinPoint joinPoint) {
        String className = joinPoint.getSignature().getDeclaringTypeName();
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        
        return className + "." + methodName + ":" + Arrays.toString(args);
    }
}

// 어노테이션
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Cacheable {
    String key() default "";
    int ttl() default 300;  // seconds
}
```

### 재시도 Aspect

```java
@Aspect
@Component
@Slf4j
public class RetryAspect {
    
    @Around("@annotation(retry)")
    public Object retryOnFailure(ProceedingJoinPoint joinPoint, Retry retry) throws Throwable {
        int maxAttempts = retry.maxAttempts();
        long delay = retry.delay();
        
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return joinPoint.proceed();
            } catch (Exception e) {
                if (attempt == maxAttempts) {
                    log.error("Failed after {} attempts", maxAttempts);
                    throw e;
                }
                
                log.warn("Attempt {} failed, retrying in {}ms", attempt, delay);
                Thread.sleep(delay);
            }
        }
        
        throw new RuntimeException("Should not reach here");
    }
}

// 어노테이션
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Retry {
    int maxAttempts() default 3;
    long delay() default 1000;  // milliseconds
}

// 사용
@Service
public class ExternalApiService {
    
    @Retry(maxAttempts = 5, delay = 2000)
    public UserResponse callExternalApi(Long id) {
        // 외부 API 호출
    }
}
```

### 권한 검사 Aspect

```java
@Aspect
@Component
@Slf4j
@RequiredArgsConstructor
public class SecurityAspect {
    
    private final UserContextHolder userContextHolder;
    
    @Before("@annotation(requireRole)")
    public void checkPermission(JoinPoint joinPoint, RequireRole requireRole) {
        User currentUser = userContextHolder.getCurrentUser();
        
        if (currentUser == null) {
            throw new UnauthorizedException("인증이 필요합니다");
        }
        
        Role[] requiredRoles = requireRole.value();
        boolean hasRole = Arrays.stream(requiredRoles)
                .anyMatch(role -> role == currentUser.getRole());
        
        if (!hasRole) {
            log.warn("Access denied for user {} to {}",
                currentUser.getEmail(),
                joinPoint.getSignature().toShortString());
            throw new ForbiddenException("권한이 없습니다");
        }
    }
}

// 어노테이션
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireRole {
    Role[] value();
}

// 사용
@Service
public class AdminService {
    
    @RequireRole(Role.ADMIN)
    public void deleteUser(Long userId) {
        // 관리자만 실행 가능
    }
}
```

### 트랜잭션 로깅 Aspect

```java
@Aspect
@Component
@Slf4j
public class TransactionLoggingAspect {
    
    @Before("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void logTransactionStart(JoinPoint joinPoint) {
        log.info("[Transaction Start] {}", joinPoint.getSignature().toShortString());
    }
    
    @AfterReturning("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void logTransactionCommit(JoinPoint joinPoint) {
        log.info("[Transaction Commit] {}", joinPoint.getSignature().toShortString());
    }
    
    @AfterThrowing("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void logTransactionRollback(JoinPoint joinPoint) {
        log.error("[Transaction Rollback] {}", joinPoint.getSignature().toShortString());
    }
}
```

## Pointcut 재사용

```java
@Aspect
@Component
public class CommonPointcuts {
    
    @Pointcut("execution(* com.example.service..*.*(..))")
    public void serviceLayer() {}
    
    @Pointcut("execution(* com.example.controller..*.*(..))")
    public void controllerLayer() {}
    
    @Pointcut("execution(* com.example.repository..*.*(..))")
    public void repositoryLayer() {}
    
    @Pointcut("serviceLayer() || controllerLayer()")
    public void applicationLayer() {}
}

@Aspect
@Component
@Slf4j
public class LoggingAspect {
    
    @Around("com.example.aspect.CommonPointcuts.serviceLayer()")
    public Object logServiceMethods(ProceedingJoinPoint joinPoint) throws Throwable {
        // 서비스 레이어 로깅
        return joinPoint.proceed();
    }
    
    @Around("com.example.aspect.CommonPointcuts.controllerLayer()")
    public Object logControllerMethods(ProceedingJoinPoint joinPoint) throws Throwable {
        // 컨트롤러 레이어 로깅
        return joinPoint.proceed();
    }
}
```

## 파라미터 접근

```java
@Aspect
@Component
@Slf4j
public class ParameterLoggingAspect {
    
    @Before("execution(* com.example.service.UserService.*(..)) && args(userId,..)")
    public void logUserId(Long userId) {
        log.info("Method called with userId: {}", userId);
    }
    
    @Around("@annotation(loggable)")
    public Object logParameters(ProceedingJoinPoint joinPoint, Loggable loggable) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        
        log.info("[{}] Parameters: {}", methodName, Arrays.toString(args));
        
        Object result = joinPoint.proceed();
        
        log.info("[{}] Result: {}", methodName, result);
        
        return result;
    }
}
```

## 실전 팁

### 1. Aspect 순서

```java
@Aspect
@Component
@Order(1)  // 숫자가 작을수록 먼저 실행
public class FirstAspect {
}

@Aspect
@Component
@Order(2)
public class SecondAspect {
}
```

### 2. 조건부 Aspect

```java
@Aspect
@Component
@ConditionalOnProperty(name = "app.logging.enabled", havingValue = "true")
public class LoggingAspect {
    // app.logging.enabled=true일 때만 활성화
}
```

### 3. 성능 고려

```java
// ❌ 나쁜 예: 모든 메서드에 적용
@Around("execution(* *(..))")

// ✅ 좋은 예: 필요한 메서드만
@Around("@annotation(com.example.annotation.Monitored)")
```

### 4. 예외 처리

```java
@Around("execution(* com.example.service.*.*(..))")
public Object handleException(ProceedingJoinPoint joinPoint) throws Throwable {
    try {
        return joinPoint.proceed();
    } catch (BusinessException e) {
        log.error("Business exception in {}: {}", 
            joinPoint.getSignature(), e.getMessage());
        throw e;  // 비즈니스 예외는 그대로 전파
    } catch (Exception e) {
        log.error("Unexpected exception in {}", 
            joinPoint.getSignature(), e);
        throw new SystemException("시스템 오류", e);
    }
}
```

## 다음 단계

AOP를 배웠습니다. 이제 Filter/Interceptor/AOP 비교를 알아봅시다.

👉 [다음: Filter vs Interceptor vs AOP](25-comparison.md)

## 참고 자료

- [Spring AOP](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop)
- [AspectJ](https://www.eclipse.org/aspectj/)
- [AOP Pointcut Expressions](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop-pointcuts)

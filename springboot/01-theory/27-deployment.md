# 배포 (Deployment)

Spring Boot 애플리케이션을 다양한 환경에 배포하는 방법을 알아봅니다.

## JAR 빌드

### Maven

```bash
mvn clean package
# 또는 테스트 제외
mvn clean package -DskipTests
```

**결과:**
```
target/my-app-1.0.0.jar
```

### Gradle

```bash
./gradlew clean build
# 또는 테스트 제외
./gradlew clean build -x test
```

**결과:**
```
build/libs/my-app-1.0.0.jar
```

## 실행

### 기본 실행

```bash
java -jar my-app-1.0.0.jar
```

### 프로파일 지정

```bash
java -jar my-app-1.0.0.jar --spring.profiles.active=prod
```

### JVM 옵션

```bash
java -Xms512m -Xmx2048m -jar my-app-1.0.0.jar
```

### 환경 변수

```bash
export DATABASE_URL=jdbc:mysql://prod-db:3306/mydb
export DATABASE_USERNAME=prod_user
export DATABASE_PASSWORD=secret
java -jar my-app-1.0.0.jar
```

## Docker 배포

### Dockerfile

```dockerfile
# Multi-stage build
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# 비root 사용자 생성
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# JAR 복사
COPY --from=build /app/target/*.jar app.jar

# 환경 변수
ENV JAVA_OPTS="-Xms512m -Xmx1024m"
ENV SPRING_PROFILES_ACTIVE=prod

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/actuator/health || exit 1

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
```

### 빌드 및 실행

```bash
# 이미지 빌드
docker build -t my-app:1.0.0 .

# 컨테이너 실행
docker run -d \
  --name my-app \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e DATABASE_URL=jdbc:mysql://db:3306/mydb \
  -e DATABASE_USERNAME=user \
  -e DATABASE_PASSWORD=password \
  my-app:1.0.0

# 로그 확인
docker logs -f my-app

# 중지
docker stop my-app

# 삭제
docker rm my-app
```

## Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    image: my-app:1.0.0
    container_name: my-app
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DATABASE_URL=jdbc:mysql://db:3306/mydb
      - DATABASE_USERNAME=root
      - DATABASE_PASSWORD=secret
      - REDIS_HOST=redis
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    restart: unless-stopped
  
  db:
    image: mysql:8.0
    container_name: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=secret
      - MYSQL_DATABASE=mydb
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
  
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mysql-data:
```

**실행:**
```bash
# 시작
docker-compose up -d

# 로그
docker-compose logs -f app

# 중지
docker-compose down

# 볼륨까지 삭제
docker-compose down -v
```

## Kubernetes 배포

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: DATABASE_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 5
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  application.yml: |
    spring:
      application:
        name: my-app
      datasource:
        hikari:
          maximum-pool-size: 20
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  url: jdbc:mysql://mysql:3306/mydb
  username: root
  password: secret
```

**배포:**
```bash
# 배포
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# 상태 확인
kubectl get pods
kubectl get services
kubectl describe pod my-app-xxxx

# 로그
kubectl logs -f my-app-xxxx

# 스케일링
kubectl scale deployment my-app --replicas=5

# 롤링 업데이트
kubectl set image deployment/my-app my-app=my-app:1.0.1

# 롤백
kubectl rollout undo deployment/my-app

# 삭제
kubectl delete deployment my-app
kubectl delete service my-app-service
```

## AWS 배포

### Elastic Beanstalk

```bash
# EB CLI 설치
pip install awsebcli

# 초기화
eb init

# 환경 생성 및 배포
eb create my-app-env
eb deploy

# 로그
eb logs

# 환경 변수 설정
eb setenv DATABASE_URL=jdbc:mysql://...
eb setenv DATABASE_USERNAME=user
eb setenv DATABASE_PASSWORD=password

# 종료
eb terminate my-app-env
```

### ECS (Fargate)

```yaml
# task-definition.json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "123456789.dkr.ecr.ap-northeast-2.amazonaws.com/my-app:1.0.0",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SPRING_PROFILES_ACTIVE",
          "value": "prod"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "ap-northeast-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Build with Maven
      run: mvn clean package -DskipTests
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: myrepo/my-app:${{ github.sha }},myrepo/my-app:latest
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/my-app my-app=myrepo/my-app:${{ github.sha }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  MAVEN_CLI_OPTS: "-s .m2/settings.xml --batch-mode"
  MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository"

build:
  stage: build
  image: maven:3.9-eclipse-temurin-17
  script:
    - mvn $MAVEN_CLI_OPTS clean package -DskipTests
  artifacts:
    paths:
      - target/*.jar

test:
  stage: test
  image: maven:3.9-eclipse-temurin-17
  script:
    - mvn $MAVEN_CLI_OPTS test

deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t my-app:$CI_COMMIT_SHA .
    - docker tag my-app:$CI_COMMIT_SHA my-app:latest
    - docker push my-app:$CI_COMMIT_SHA
    - docker push my-app:latest
  only:
    - main
```

## 무중단 배포

### Blue-Green 배포

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:1.0.0

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-app:1.0.1

---
# service.yaml (blue 또는 green으로 전환)
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: blue  # 또는 green으로 변경
  ports:
  - port: 80
    targetPort: 8080
```

### Canary 배포

```yaml
# stable-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: my-app
      track: stable

---
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
spec:
  replicas: 1  # 10% 트래픽
  selector:
    matchLabels:
      app: my-app
      track: canary
```

## 모니터링

### Prometheus + Grafana

```yaml
# docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'spring-boot'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['app:8080']
```

## 실전 팁

### 1. 프로덕션 체크리스트

```yaml
✅ 환경별 설정 분리 (local, dev, prod)
✅ 민감 정보 환경 변수화
✅ 로깅 설정 (파일, 로테이션)
✅ 헬스 체크 엔드포인트
✅ 메트릭 수집
✅ 에러 추적 (Sentry 등)
✅ 백업 전략
✅ 롤백 계획
```

### 2. JVM 튜닝

```bash
java \
  -Xms1g \
  -Xmx2g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/logs/heapdump.hprof \
  -jar app.jar
```

### 3. 로깅 설정

```yaml
# application-prod.yml
logging:
  level:
    root: INFO
    com.example: INFO
  file:
    name: /var/log/app/application.log
  logback:
    rollingpolicy:
      max-file-size: 100MB
      max-history: 30
      total-size-cap: 3GB
```

### 4. Graceful Shutdown

```yaml
# application.yml
server:
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

### 5. 배포 전 체크

```bash
# 헬스 체크
curl http://localhost:8080/actuator/health

# 애플리케이션 정보
curl http://localhost:8080/actuator/info

# 메트릭 확인
curl http://localhost:8080/actuator/metrics

# 로그 레벨 확인
curl http://localhost:8080/actuator/loggers
```

## 다음 단계

Spring Boot 이론을 모두 배웠습니다! 이제 실습으로 넘어가세요.

👉 [실습 시작](../02-practice/README.md)

## 참고 자료

- [Spring Boot Deployment](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment.html)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS Documentation](https://aws.amazon.com/documentation/)

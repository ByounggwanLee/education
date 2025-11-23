# React 개발 환경

VS Code에서 React(Vite)를 사용한 프론트엔드 개발 환경 설정과 효율적인 개발 방법을 알아봅니다.

## 사전 준비

### 필수 설치 항목

1. **Node.js (LTS 버전)**
   ```bash
   node --version  # v18.x 이상 권장
   npm --version   # v9.x 이상 권장
   ```
   
   [Node.js 공식 사이트](https://nodejs.org/)에서 다운로드

2. **필수 VS Code 확장**
   - ES7+ React/Redux/React-Native snippets
   - ESLint
   - Prettier - Code formatter
   - Auto Rename Tag
   - Path Intellisense

3. **선택적 확장**
   - Vite
   - CSS Modules
   - Tailwind CSS IntelliSense (Tailwind 사용 시)
   - styled-components (styled-components 사용 시)

## React 프로젝트 생성 (Vite)

### Vite로 프로젝트 생성

```bash
# npm 사용
npm create vite@latest my-react-app -- --template react

# 또는 TypeScript 템플릿
npm create vite@latest my-react-app -- --template react-ts

# 프로젝트 폴더로 이동
cd my-react-app

# 의존성 설치
npm install

# 개발 서버 시작
npm run dev
```

### 프로젝트 구조

```
my-react-app/
├── node_modules/          # 의존성
├── public/                # 정적 파일
│   └── vite.svg
├── src/
│   ├── assets/           # 이미지, 폰트 등
│   ├── components/       # 재사용 컴포넌트
│   ├── pages/            # 페이지 컴포넌트
│   ├── hooks/            # 커스텀 훅
│   ├── utils/            # 유틸리티 함수
│   ├── styles/           # 전역 스타일
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── .eslintrc.cjs         # ESLint 설정
├── .gitignore
├── index.html            # 진입점 HTML
├── package.json          # 프로젝트 설정
├── vite.config.js        # Vite 설정
└── README.md
```

## VS Code 프로젝트 설정

### 워크스페이스 설정

`.vscode/settings.json`:
```json
{
  // 포맷팅
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  
  // JavaScript/TypeScript
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  
  // CSS
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  
  // Import 자동 정리
  "editor.formatOnPaste": false,
  "javascript.updateImportsOnFileMove.enabled": "always",
  "typescript.updateImportsOnFileMove.enabled": "always",
  
  // Emmet
  "emmet.includeLanguages": {
    "javascript": "javascriptreact",
    "typescript": "typescriptreact"
  },
  "emmet.triggerExpansionOnTab": true
}
```

### 권장 확장 프로그램

`.vscode/extensions.json`:
```json
{
  "recommendations": [
    "dsznajder.es7-react-js-snippets",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "antfu.vite",
    "bradlc.vscode-tailwindcss"
  ]
}
```

## ESLint 설정

### ESLint 설치 및 설정

```bash
# ESLint 및 플러그인 설치
npm install -D eslint eslint-plugin-react eslint-plugin-react-hooks
```

`.eslintrc.cjs`:
```javascript
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  plugins: ['react', 'react-hooks'],
  rules: {
    'react/react-in-jsx-scope': 'off', // React 17+에서 불필요
    'react/prop-types': 'off',
    'no-unused-vars': 'warn',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn'
  },
  settings: {
    react: {
      version: 'detect'
    }
  }
}
```

## Prettier 설정

`.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

`.prettierignore`:
```
node_modules
dist
build
.vite
coverage
```

## 개발 서버 실행

### 방법 1: package.json 스크립트 사용

```bash
npm run dev    # 개발 서버 시작
npm run build  # 프로덕션 빌드
npm run preview # 빌드 결과 미리보기
```

### 방법 2: VS Code Tasks

`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Dev Server",
      "type": "npm",
      "script": "dev",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Build",
      "type": "npm",
      "script": "build",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": []
    }
  ]
}
```

실행: `Ctrl+Shift+B` → "Start Dev Server" 선택

### 방법 3: NPM Scripts 뷰

1. Explorer에서 "NPM SCRIPTS" 섹션 확인
2. 원하는 스크립트 옆의 ▶️ 버튼 클릭

## React 코드 작성

### 컴포넌트 생성 스니펫

**함수형 컴포넌트 (rafce):**
```javascript
// rafce 입력 후 Tab
import React from 'react'

const ComponentName = () => {
  return (
    <div>ComponentName</div>
  )
}

export default ComponentName
```

**주요 스니펫:**
- `rafce` → React Arrow Function Component Export
- `rafc` → React Arrow Function Component
- `rfc` → React Function Component
- `useS` → useState Hook
- `useE` → useEffect Hook
- `useC` → useContext Hook
- `useCB` → useCallback Hook
- `useM` → useMemo Hook
- `useR` → useRef Hook

### 컴포넌트 예시

`src/components/UserList.jsx`:
```jsx
import { useState, useEffect } from 'react'
import './UserList.css'

const UserList = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/users')
      const data = await response.json()
      setUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div className="user-list">
      <h1>사용자 목록</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.name} - {user.email}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default UserList
```

### IntelliSense 활용

- **자동 완성**: `Ctrl+Space`
- **Import 자동 추가**: 컴포넌트 입력 시 자동으로 import 제안
- **Props 자동 완성**: JSX에서 props 입력 시 자동 완성
- **Emmet**: `div.container>ul>li*5` → Tab

## CSS 관리

### 일반 CSS

```jsx
import './Component.css'
```

### CSS Modules

`Component.module.css`:
```css
.container {
  padding: 20px;
}

.title {
  font-size: 24px;
  color: #333;
}
```

컴포넌트에서 사용:
```jsx
import styles from './Component.module.css'

const Component = () => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>제목</h1>
    </div>
  )
}
```

### Tailwind CSS (선택사항)

설치:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

`tailwind.config.js`:
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

`src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## 라우팅 (React Router)

### 설치

```bash
npm install react-router-dom
```

### 설정

`src/App.jsx`:
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import About from './pages/About'
import UserList from './components/UserList'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<UserList />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

## 상태 관리

### Context API

`src/context/AuthContext.jsx`:
```jsx
import { createContext, useContext, useState } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)

  const login = (userData) => {
    setUser(userData)
  }

  const logout = () => {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
```

## API 호출

### Axios 사용

설치:
```bash
npm install axios
```

`src/api/userApi.js`:
```javascript
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8080/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const userApi = {
  getAll: () => api.get('/users'),
  getById: (id) => api.get(`/users/${id}`),
  create: (user) => api.post('/users', user),
  update: (id, user) => api.put(`/users/${id}`, user),
  delete: (id) => api.delete(`/users/${id}`),
}
```

## 빌드 및 배포

### 프로덕션 빌드

```bash
npm run build
```

빌드 결과: `dist/` 폴더

### 환경 변수

`.env`:
```
VITE_API_URL=http://localhost:8080
```

`.env.production`:
```
VITE_API_URL=https://api.production.com
```

사용:
```javascript
const apiUrl = import.meta.env.VITE_API_URL
```

### Vite 설정

`vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
```

## 디버깅

React 컴포넌트 디버깅은 다음 챕터에서 자세히 다룹니다.

간단한 디버깅:
1. Chrome DevTools 사용
2. `console.log()` 대신 `debugger` 사용
3. React DevTools 확장 설치

## 성능 최적화

### React.memo

```jsx
import { memo } from 'react'

const ExpensiveComponent = memo(({ data }) => {
  // 컴포넌트 로직
  return <div>{data}</div>
})
```

### useMemo와 useCallback

```jsx
import { useMemo, useCallback } from 'react'

const Component = ({ items }) => {
  const filteredItems = useMemo(() => {
    return items.filter(item => item.active)
  }, [items])

  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])

  return <div>{/* ... */}</div>
}
```

## 유용한 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+Space` | 자동 완성 |
| `F2` | 심볼 이름 변경 (모든 참조 포함) |
| `Alt+Shift+F` | 파일 포맷팅 |
| `Ctrl+/` | 주석 토글 |
| `Alt+↑/↓` | 줄 이동 |
| `Shift+Alt+↓` | 줄 복사 |

## 문제 해결

### ESLint 오류 무시

파일 상단에 추가:
```javascript
/* eslint-disable */
```

특정 줄만:
```javascript
// eslint-disable-next-line react-hooks/exhaustive-deps
```

### 모듈을 찾을 수 없음

```bash
# node_modules 재설치
rm -rf node_modules package-lock.json
npm install
```

### 핫 리로드가 작동하지 않음

`vite.config.js`:
```javascript
export default defineConfig({
  server: {
    watch: {
      usePolling: true,
    },
  },
})
```

## 다음 단계

이제 디버깅 기초를 알아봅시다.

👉 [다음: 디버깅 기초](07-debugging-basics.md)

## 참고 자료

- [Vite 공식 문서](https://vitejs.dev/)
- [React 공식 문서](https://react.dev/)
- [React Router 문서](https://reactrouter.com/)

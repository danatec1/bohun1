# 데이터 분석 대시보드

React + TypeScript + Tailwind CSS + Recharts로 구축된 인터랙티브 차트 대시보드입니다.

## 기능

- 7가지 다양한 차트 유형 (막대 차트, 라인 차트, 파이 차트, 영역 차트 등)
- 수직 캐러셀 네비게이션
- 반응형 디자인
- 다크 모드 지원
- 인터랙티브 차트 툴팁

## 시작하기

### 필수 요구사항

- Node.js 18.0 이상
- npm 또는 yarn 또는 pnpm

### 설치

1. 프로젝트 디렉토리로 이동:
```bash
cd data-dashboard
```

2. 의존성 패키지 설치:
```bash
npm install
```

또는 yarn 사용:
```bash
yarn install
```

또는 pnpm 사용:
```bash
pnpm install
```

### 개발 서버 실행

```bash
npm run dev
```

브라우저에서 `http://localhost:5173`을 열어 확인하세요.

### 빌드

프로덕션 빌드를 생성하려면:
```bash
npm run build
```

빌드된 파일은 `dist` 폴더에 생성됩니다.

### 프리뷰

빌드된 앱을 미리보기:
```bash
npm run preview
```

## 프로젝트 구조

```
├── App.tsx                 # 메인 애플리케이션 컴포넌트
├── main.tsx               # React 앱 엔트리 포인트
├── index.html             # HTML 템플릿
├── components/
│   ├── ui/               # ShadCN UI 컴포넌트들
│   └── figma/            # Figma 관련 컴포넌트
├── styles/
│   └── globals.css       # 전역 스타일 및 Tailwind 설정
├── package.json          # 프로젝트 의존성
├── vite.config.ts        # Vite 설정
└── tsconfig.json         # TypeScript 설정
```

## 사용된 기술

- **React 18** - UI 라이브러리
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구
- **Tailwind CSS v4** - 스타일링
- **Recharts** - 차트 라이브러리
- **ShadCN UI** - UI 컴포넌트 라이브러리
- **Lucide React** - 아이콘
- **Embla Carousel** - 캐러셀 기능

## 커스터마이징

### 차트 데이터 수정

`App.tsx` 파일에서 차트 데이터를 수정할 수 있습니다:

```typescript
const salesData = [
  { month: "1월", sales: 4200, target: 4000 },
  // 여기에 데이터를 추가하거나 수정하세요
];
```

### 색상 테마 변경

`styles/globals.css` 파일에서 CSS 변수를 수정하여 색상을 변경할 수 있습니다:

```css
:root {
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  /* 원하는 색상으로 변경 */
}
```

### 새로운 차트 추가

`App.tsx`의 `charts` 배열에 새로운 차트 객체를 추가하세요:

```typescript
{
  id: 7,
  title: "새로운 차트",
  description: "설명",
  icon: YourIcon,
  component: (
    <ChartContainer config={chartConfig}>
      {/* 차트 컴포넌트 */}
    </ChartContainer>
  ),
}
```

## 라이선스

MIT

## 문의

문제가 발생하거나 질문이 있으시면 이슈를 등록해주세요.

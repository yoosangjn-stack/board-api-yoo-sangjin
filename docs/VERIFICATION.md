# 분리본 검증 기록

기준: 2026-11-16. 기존 쇼핑몰 및 LAP의 과거 검증 결과와 구분합니다.

## 통과
- `uv sync`: 설치 및 잠금파일 갱신 완료. FastAPI 필수 라이브러리와 uvicorn만 사용해 불필요한 CLI 부가 의존성을 제외.
- `ruff check src tests scripts`: 통과
- 구조 및 JWT·bcrypt 단위 테스트: 10 passed, 39 deselected
- ASGI HTTP 검사: `/health`, `/docs`, `/openapi.json` 각각 200
- OpenAPI 경로에서 상품·주문 엔드포인트가 제거됨을 확인
- SQLAlchemy metadata에 `users`, `token_blacklist`, `boards`, `posts`, `comments`만 등록됨을 확인

## 아직 실행하지 않음
- PostgreSQL 서버를 이용한 전체 통합 테스트: 현재 검증 환경에 PostgreSQL 서버 없음
- 실제 브라우저 Swagger CRUD, 외부 네트워크 접속
- EC2 배포, 실제 시연 캡처, LMS 제출

## 재검증 절차

별도 빈 로컬 DB `board_test`를 준비하고 `TEST_DATABASE_URL`을 지정한 후 `uv run pytest -q` 실행.
모든 결과가 통과하면 실제 `board_app` 학습 DB로 Swagger 시연 순서를 수행하고 캡처를 추가합니다.
테스트 실패를 숨기거나 미실행을 통과로 기록하지 않습니다.

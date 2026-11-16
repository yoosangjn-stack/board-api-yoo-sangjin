# Board API

유상진 개인 CH3 평가 과제. Premium Food API에서 회원·인증·게시판 기능만 분리한 REST API입니다.

## 1. 목적과 범위

게시글을 저장하는 것에서 끝나지 않고 **누가 작성했고, 누가 수정할 수 있는지**까지 검증합니다.
회원가입 → 로그인 → 글 작성 → 조회 → 수정 → 삭제가 핵심 흐름입니다.

- 포함: 회원가입, JWT 로그인·로그아웃, 게시판·게시글·댓글 CRUD, 작성자/관리자 권한, 검색·페이지 처리
- 제외: 상품, 주문, 재고, 쇼핑몰 화면. 별도 프론트엔드 없이 Swagger UI로 확인합니다.
- DB: PostgreSQL + SQLAlchemy / API: FastAPI + Pydantic / 인증: PyJWT + bcrypt

## 2. 4계층

| 계층 | 역할 | 예시 |
|---|---|---|
| Presentation | 요청을 받고 입력·응답 형식 검증 | `board/presentation/router.py` |
| Application | 기능의 순서와 권한·트랜잭션 조정 | `board/application/service.py` |
| Domain | 게시글 규칙과 저장소 인터페이스 | `board/domain/post.py` |
| Infrastructure | SQLAlchemy로 실제 DB 저장·조회 | `board/infrastructure/repositories.py` |

요청은 Router → Service → Repository 구현 → PostgreSQL로 처리됩니다.
Domain은 FastAPI·SQLAlchemy를 모릅니다. `wiring/`이 인터페이스와 구현을 연결합니다.

```text
src/
  main.py                 실행 진입점
  database.py             DB 연결과 요청별 세션
  user/                   회원 4계층
  auth/                   인증 4계층
  board/                  게시판 4계층
  shared/                 공통 오류·응답·트랜잭션
  wiring/                 의존성 연결
```

## 3. 데이터 관계

```mermaid
erDiagram
  users ||--o{ posts : writes
  users ||--o{ comments : writes
  boards ||--o{ posts : contains
  posts ||--o{ comments : contains
  users { uuid id PK }
  boards { string id PK }
  posts { bigint id PK
          string board_id FK
          uuid author_id FK }
  comments { bigint id PK
             bigint post_id FK
             uuid author_id FK }
  token_blacklist { string jti PK }
```

게시글·댓글은 작성자 외 수정·삭제를 제한합니다. 관리자에게는 관리 권한이 있습니다.
비밀번호는 해시로 저장하고, 만료·로그아웃된 토큰은 거절합니다. 기본 자유 게시판은 로그인 후 작성합니다.

## 4. 실행: Windows PowerShell

Python 3.13+, uv, PostgreSQL이 필요합니다. **기존 쇼핑몰 DB가 아닌 빈 `board_app` DB**를 준비하세요.

```powershell
uv sync --frozen
Copy-Item .env.example .env
uv run python -c "import secrets; print(secrets.token_urlsafe(64))"
```

마지막 명령의 임의 값을 `.env`의 `JWT_SECRET_KEY`에 저장합니다. 공유하거나 커밋하지 않습니다.
`DATABASE_URL`은 본인의 새 DB 계정으로 입력합니다. 첫 학습 실행에만 `CREATE_TABLES=true`, `DEMO_SEED=true`를 지정하면 테이블과 `free` 게시판이 생성됩니다. 이후 `CREATE_TABLES=false`, `DEMO_SEED=false`로 돌려놓습니다.

```powershell
$env:PYTHONPATH="src"
uv run uvicorn main:app --app-dir src --host 127.0.0.1 --port 8000
```

- Swagger: http://127.0.0.1:8000/docs
- 명세 원문: http://127.0.0.1:8000/openapi.json
- 상태 확인: http://127.0.0.1:8000/health

`/health`는 프로세스 확인용입니다. DB 연결 정상 여부를 보장하지 않습니다.

## 5. 시연 순서

1. `POST /v1/users`: 서로 다른 회원 A, B 가입
2. Swagger **Authorize**: username에 A의 이메일, password에 비밀번호 입력
3. `POST /v1/boards/free/posts`: 제목·내용 등록 (201)
4. 목록 및 상세 조회 (200)
5. 작성자 A로 수정 (200)
6. 회원 B로 인증 후 같은 글 수정·삭제 요청 (403)
7. A로 다시 인증한 뒤 삭제 (204), 이후 조회 거절 확인
8. 댓글 CRUD 및 로그아웃 후 토큰 거절 확인

Swagger의 각 요청 스키마와 상태코드는 [API 명세](docs/API_SPEC.md)를 참고합니다.
캡처에는 비밀번호·토큰·실제 연락처를 노출하지 않습니다.

## 6. 검증

```powershell
$env:TEST_DATABASE_URL="postgresql+asyncpg://<테스트계정>:<비밀번호>@127.0.0.1:5432/board_test"
uv run pytest -q
uv run ruff check src tests scripts
```

테스트는 **localhost의 `board_test` 전용 DB만 허용**하며, 테스트별 변경을 롤백합니다. 다른 업무 데이터가 없는 계정·DB를 사용하세요.
[기존 검증 기록](docs/VERIFICATION.md)은 배포 전 기록입니다. 아래 2026-11-16 결과가 최신입니다. 과거 쇼핑몰의 테스트 통과 수는 이 분리본의 결과가 아닙니다.

## 7. 배포 및 최신 검증 (2026-11-16 KST)

- 공개 저장소: https://github.com/yoosangjn-stack/board-api-yoo-sangjin
- **AWS EC2 Swagger:** http://15.164.231.147/docs
- API 명세: http://15.164.231.147/openapi.json
- 상태 확인: http://15.164.231.147/health
- 서울 리전 Ubuntu / t3.micro / Nginx → FastAPI / PostgreSQL 구성입니다.
- DB 5432와 앱 8000은 localhost에만 바인딩합니다. 공개 웹은 80, SSH 22는 관리용 IP 한 곳만 허용합니다.
- 무료 플랜 크레딧으로 실행하며 유료 플랜으로 전환하지 않았습니다. 영구 무료 서비스는 아닙니다. 인스턴스 중지·재시작 시 공인 IP가 달라질 수 있습니다.
- HTTP 학습용 서비스이므로 실제 개인정보나 다른 서비스에서 사용하는 비밀번호를 입력하지 마세요.

### 오늘 실제 확인한 결과

- 이 저장소의 PostgreSQL 전용 테스트 DB에서 전체 pytest **58개 통과**, Ruff 통과. 과거 쇼핑몰 결과가 아닙니다.
- 테스트의 CORS 검증은 localhost Origin을 사용합니다. 운영 환경의 공개 IP Origin과 구분하여 테스트 프로세스에서 설정합니다.
- 노트북에서 외부 HTTP 요청으로 /health, /docs, /openapi.json 각각 200 확인.
- 가짜 테스트 계정으로 회원가입(201), JWT 로그인, 게시글 생성·조회·수정·삭제(204), 로그아웃(204)을 실제 외부 API로 확인했습니다. 테스트 게시글은 삭제했습니다.
- 서비스 재시작 후 응답 확인. 초기 테이블/데모 생성 옵션은 false로 돌려놓았습니다.
- .env.example, .gitignore, .python-version 보완 완료. 실제 .env 및 SSH 개인키는 저장소에 없습니다.

### 남은 확인

- [x] 실제 Chrome에서 Swagger UI 정상 표시 확인
- [ ] 과제 제출용 화면 캡처 파일 첨부
- [ ] 사용자의 LMS 최종 제출 확인

초기 브라우저 타임아웃은 https:// 주소로 접속한 것이 원인이었습니다. http://15.164.231.147/docs 로 변경하여 실제 Chrome에서 Swagger UI 정상 표시를 확인했습니다. HTTPS는 구성하지 않았으므로 반드시 HTTP 주소를 사용하세요. 화면 표시 확인과 전체 브라우저 CRUD 시연·캡처 첨부는 구분합니다.

## 8. 기반 코드

- [Premium Food API](https://github.com/yoosangjn-stack/premium-food-api), 기준 커밋 `38c3c50e1a059788db824630e8b01599e891db32`
- [강의 게시판 프로젝트](https://github.com/yonggyo1125/backend_project_ax1)

분리 과정에서는 회원·인증·게시판 구조를 유지하고 상품·주문·템플릿·정적 UI를 제거했습니다.

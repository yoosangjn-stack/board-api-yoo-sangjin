# API 명세

실제 FastAPI OpenAPI에서 생성한 엔드포인트 목록입니다. 요청·응답 상세는 `openapi.json`과 실행 중 `/docs`에서 확인합니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | `/v1/users` | 회원가입 |
| PATCH | `/v1/users/{user_id}/password` | 비밀번호 변경 |
| POST | `/v1/auth/login` | 로그인 |
| POST | `/v1/auth/logout` | 로그아웃 |
| POST | `/v1/auth/token` | OAuth2 토큰 발급 |
| POST | `/v1/boards` | 게시판 생성 |
| GET | `/v1/boards` | 게시판 전체 목록 조회 |
| GET | `/v1/boards/{board_id}` | 게시판 단건 상세 조회 |
| PUT | `/v1/boards/{board_id}` | 게시판 설정 수정 (관리자 전용) |
| DELETE | `/v1/boards/{board_id}` | 게시판 삭제 (관리자 전용) |
| POST | `/v1/boards/{board_id}/posts` | 게시글 작성 |
| GET | `/v1/boards/{board_id}/posts` | 게시글 목록 페이징 및 검색 |
| GET | `/v1/posts/{post_id}` | 게시글 상세 조회 |
| PUT | `/v1/posts/{post_id}` | 게시글 수정 |
| DELETE | `/v1/posts/{post_id}` | 게시글 삭제 |
| POST | `/v1/posts/{post_id}/comments` | 댓글 작성 |
| GET | `/v1/posts/{post_id}/comments` | 게시글의 댓글 목록 조회 |
| PUT | `/v1/comments/{comment_id}` | 댓글 수정 |
| DELETE | `/v1/comments/{comment_id}` | 댓글 삭제 |
| GET | `/health` | Health |

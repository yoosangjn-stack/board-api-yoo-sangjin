"""DEMO_SEED=true일 때 새 자유 게시판만 생성합니다. 기존 자료는 변경하지 않습니다."""
from board.infrastructure.models import BoardModel

async def seed_demo_data(session) -> None:
    if await session.get(BoardModel, "free") is None:
        session.add(BoardModel(board_id="free", board_name="자유 게시판",
                               page_size=20, edit_role="USER", comment_edit_role="USER"))
    await session.commit()

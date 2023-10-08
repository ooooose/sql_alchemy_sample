from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

"""
データベースの接続情報を設定

入力例は以下のとおり
DATABASE_URL = "postgresql://username:password@localhost/database_name"
"""
DATABASE_URL = "postgresql://postgres:password@postgres-db:5432/postgres"

# データベースエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションファクトリを作成
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルを定義するための基本となるBaseクラスを作成
Base = declarative_base()

# セッションを依存性として定義
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from table_user import User
from table_post import Post


class Feed(Base):
    __tablename__ = "feed_action"
    __table_args__ = {"schema":"public"}

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)

    user = relationship(User)
    post = relationship(Post)

    action = Column(String)
    time = Column(TIMESTAMP)

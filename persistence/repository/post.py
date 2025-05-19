from flask import g


class PostRepository:
    @staticmethod
    def find_all():
        statement = (
            Post
            .select().order_by(Post.id.desc())
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_id(post_id: int):
        statement = (
            Post
            .select()
            .where(Post.id == post_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def filter(query_string: str, ascending: bool):
        query = g.session.query(Post)

        if query_string:
            query = query.filter(Post.content.contains(query_string))

        if ascending:
            query = query.order_by(Post.id)
        else:
            query = query.order_by(Post.id.desc())

        return g.session.scalars(query).all()

    @staticmethod
    def save(post):
        g.session.add(post)
        g.session.commit()

        return Post

    @staticmethod
    def delete(post) -> None:
        g.session.delete(post)
        g.session.commit()


from persistence.model.post import Post

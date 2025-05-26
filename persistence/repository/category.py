from flask import g


class CategoryRepository:
    @staticmethod
    def find_all():
        statement = (
            Category
            .select().order_by(Category.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_id(category_id: int):
        statement = (
            Category
            .select()
            .where(Category.id == category_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_by_path_slug(path_slug: str):
        statement = (
            Category
            .select()
            .where(Category.path_slug == path_slug)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_all_descendants(category_id: int):
        statement = (
            Category
            .select()
            .where(Category.path.like(f"%{category_id}/%")).order_by(Category.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_all_direct_descendants(category_id: int):
        statement = (
            Category
            .select()
            .where(Category.parent_id == category_id).order_by(Category.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_all_roots():
        statement = (
            Category
            .select()
            .where(Category.parent_id == None).order_by(Category.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_all_ancestors(category):
        ids = [int(i) for i in category.path.split('/')][:-1]
        if not ids:
            return []

        statement = (
            Category
            .select()
            .where(Category.id.in_(ids)).order_by(Category.name)
        )
        return g.session.scalars(statement).all()

    @staticmethod
    def whole_tree_for_category(category):
        ids = [int(i) for i in category.path.split('/')]
        if not ids:
            return []
        results = []

        for i in ids:
            results.append(CategoryRepository.find_by_id(i))

        return results


from persistence.model.category import Category
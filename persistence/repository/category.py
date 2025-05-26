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
        ids = category.ids[:-1]
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
        ids = category.ids
        if not ids:
            return []
        results = []

        for i in ids:
            results.append(CategoryRepository.find_by_id(i))

        return results

    @staticmethod
    def all_attributes(category):
        results = AttributeRepository.find_all_default()

        ids = category.ids
        if not ids:
            return []

        statement = (
            CategoryAttribute
            .select()
            .where(CategoryAttribute.category_id.in_(ids))
        )
        results += [attr.attribute for attr in g.session.scalars(statement).all()]
        return sorted(results, key=lambda x: x.name)

    @staticmethod
    def find_all_leafs_of_category(category):
        results = CategoryRepository.find_all_descendants(category.id)
        return [cat for cat in results if cat.is_leaf]


from persistence.model.category import Category
from persistence.repository.attribute import AttributeRepository
from persistence.model.attribute import CategoryAttribute
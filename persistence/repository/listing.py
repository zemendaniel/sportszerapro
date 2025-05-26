from flask import g


class ListingRepository:
    @staticmethod
    def find_all():
        statement = (
            Listing
            .select().order_by(Listing.id.desc())
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_id(listing_id: int):
        statement = (
            Listing
            .select()
            .where(Listing.id == listing_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_all_by_category_id(category_id: int):
        statement = (
            Listing
            .select()
            .where(Listing.category_id == category_id)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_slug(slug: str):
        statement = (
            Listing
            .select()
            .where(Listing.slug == slug)
        )

        return g.session.scalar(statement)


from persistence.model.listing import Listing

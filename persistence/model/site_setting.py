from alchemical import Model
from sqlalchemy import Integer, BLOB, String
from sqlalchemy.orm import Mapped, mapped_column


class SiteSetting(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # BLOB so that we can store anything (text, images, etc.)
    value: Mapped[str] = mapped_column(BLOB(255), nullable=False)

    def save(self):
        SiteSettingRepository.save(self)

    def delete(self):
        SiteSettingRepository.delete(self)


from persistence.repository.site_setting import SiteSettingRepository

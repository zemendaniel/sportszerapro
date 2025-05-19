from flask import g
from werkzeug.datastructures import FileStorage


class SiteSettingRepository:
    @staticmethod
    def find_by_key(key):
        return g.session.scalar(SiteSetting.select().where(SiteSetting.key == key))

    @staticmethod
    def set_org_name(name):
        org_name = SiteSettingRepository.find_by_key('org_name') or SiteSetting()
        org_name.key = 'org_name'
        org_name.value = name.encode('utf-8')
        org_name.save()

    @staticmethod
    def get_org_name():
        name = SiteSettingRepository.find_by_key('org_name')
        if name:
            return name.value.decode('utf-8')
        return "Szervezet neve"

    @staticmethod
    def set_favicon(file):
        favicon = SiteSettingRepository.find_by_key('favicon') or SiteSetting()
        favicon.key = 'favicon'
        favicon.value = file.read()
        favicon.save()

    @staticmethod
    def get_favicon():
        favicon = SiteSettingRepository.find_by_key('favicon')
        if favicon:
            file: FileStorage = favicon.value
            return file
        return None

    @staticmethod
    def delete(site_setting):
        g.session.delete(site_setting)
        g.session.commit()

    @staticmethod
    def save(site_setting):
        g.session.add(site_setting)
        g.session.commit()

    @staticmethod
    def find_by_id(setting_id):
        return g.session.scalar(SiteSetting.select().where(SiteSetting.id == setting_id))

    @staticmethod
    def get_welcome_text():
        welcome_text = SiteSettingRepository.find_by_key('welcome_text')
        if welcome_text:
            return welcome_text.value.decode('utf-8')
        return "Üdvözlő szöveg"

    @staticmethod
    def set_welcome_text(text):
        welcome_text = SiteSettingRepository.find_by_key('welcome_text') or SiteSetting()
        welcome_text.key = 'welcome_text'
        welcome_text.value = text.encode('utf-8')
        welcome_text.save()


from persistence.model.site_setting import SiteSetting

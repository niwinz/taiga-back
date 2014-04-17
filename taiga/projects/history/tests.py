from django import test
from taiga.base.users.tests import create_user
from taiga.projects.tests import create_project
from taiga.projects.userstories.tests import create_userstory

from . import services as history
from . import models


class HistoryServicesTest(test.TestCase):
    fixtures = ["initial_domains.json"]

    def setUp(self):
        self.user1 = create_user(1) # Project owner
        self.project1 = create_project(1, self.user1)

    def test_freeze_userstory(self):
        userstory1 = create_userstory(1, self.user1, self.project1)
        fobj = history.freeze_model_instance(userstory1)

        self.assertEqual(fobj.type, "userstories.userstory")
        self.assertIn("status", fobj.value)

    def test_local_persistence(self):
        userstory1 = create_userstory(1, self.user1, self.project1)
        fobj = history.freeze_model_instance(userstory1)

        key = history.make_key_from_frozen_object(fobj)
        history.store_frozen_object(key, fobj)

        fobj2 = history.get_stored_frozen_object(key)
        self.assertEqual(fobj, fobj2)

        history.clear_frozen_objects_storage()
        with self.assertRaises(KeyError):
            history.get_stored_frozen_object(key)

    def test_freeze_wrong_object(self):
        some_object = object()
        with self.assertRaises(Exception):
            history.freeze_model_instance(some_object)

    def test_diff(self):
        userstory1 = create_userstory(1, self.user1, self.project1)
        userstory1.subject = "test1"
        userstory1.save()

        fobj1 = history.freeze_model_instance(userstory1)

        userstory1.subject = "test2"
        userstory1.save()

        fobj2 = history.freeze_model_instance(userstory1)

        diff = history.make_diff(fobj1, fobj2)
        self.assertIn("subject", diff.value)
        self.assertEqual(diff.value, {"subject": ('test1', 'test2')})

    def test_freeze(self):
        userstory1 = create_userstory(1, self.user1, self.project1)
        userstory1.subject = "test1"
        userstory1.save()

        history.freeze(userstory1)

        userstory1.subject = "test2"
        userstory1.save()

        key = history.make_key_from_model_object(userstory1)
        fobj = history.get_stored_frozen_object(key)
        self.assertEqual(fobj.type, "userstories.userstory")

        self.assertEqual(models.HistoryEntry.objects.count(), 0)
        history.persist_change(userstory1)
        self.assertEqual(models.HistoryEntry.objects.count(), 1)

    def test_comment(self):
        userstory1 = create_userstory(1, self.user1, self.project1)

        self.assertEqual(models.HistoryEntry.objects.count(), 0)
        history.persist_comment(userstory1, "Sample comment")
        self.assertEqual(models.HistoryEntry.objects.count(), 1)


    def test_create(self):
        userstory1 = create_userstory(1, self.user1, self.project1)

        self.assertEqual(models.HistoryEntry.objects.count(), 0)
        history.persist_create(userstory1)
        self.assertEqual(models.HistoryEntry.objects.count(), 1)

    def test_delete(self):
        userstory1 = create_userstory(1, self.user1, self.project1)

        self.assertEqual(models.HistoryEntry.objects.count(), 0)
        history.persist_delete(userstory1)
        self.assertEqual(models.HistoryEntry.objects.count(), 1)

